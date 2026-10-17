package com.quicklab.app

import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.InputStream
import java.util.concurrent.TimeUnit

class MainActivity : ComponentActivity() {
    private val client = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(60, TimeUnit.SECONDS)
        .build()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            QuicklabApp(client = client)
        }
    }
}

@Composable
fun QuicklabApp(client: OkHttpClient) {
    var resultText by remember { mutableStateOf("No video uploaded yet") }
    var selectedFileName by remember { mutableStateOf("No file selected") }
    var timeline by remember { mutableStateOf(listOf<TimelineClip>()) }
    var captions by remember { mutableStateOf(listOf<CaptionItem>()) }
    var exportStatus by remember { mutableStateOf("Ready to export") }
    var projectId by remember { mutableStateOf("proj-0001") }

    val launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent(),
        onResult = { uri ->
            if (uri != null) {
                selectedFileName = uri.lastPathSegment ?: "selected_video.mp4"
                uploadVideo(client, projectId, uri, onResult = { responseText ->
                    resultText = responseText
                    timeline = listOf(
                        TimelineClip("clip-1", 0.0f, 3.0f, "intro", 0.94f),
                        TimelineClip("clip-2", 3.0f, 8.0f, "highlight", 0.91f),
                        TimelineClip("clip-3", 8.0f, 12.0f, "caption-shot", 0.93f),
                    )
                    captions = listOf(
                        CaptionItem("00:00-00:02", "Welcome to Quicklab"),
                        CaptionItem("00:02-00:05", "AI-powered editing starts here"),
                        CaptionItem("00:05-00:08", "Create your next short in minutes"),
                    )
                    persistProject(client, projectId, timeline, captions)
                    exportStatus = "Metadata ready"
                })
            }
        }
    )

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            verticalArrangement = Arrangement.Top,
            horizontalAlignment = Alignment.Start
        ) {
            Text("Quicklab", style = MaterialTheme.typography.headlineMedium)
            Text("AI video editor", modifier = Modifier.padding(bottom = 12.dp))

            Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                Button(onClick = { launcher.launch("video/*") }) {
                    Text("Pick Video")
                }
                Button(onClick = {
                    exportStatus = "Export queued"
                    exportVideo(client, projectId, onResult = { exportStatus = it })
                }) {
                    Text("Export")
                }
            }

            Text("Selected: $selectedFileName", modifier = Modifier.padding(top = 8.dp))
            Text(resultText, modifier = Modifier.padding(top = 8.dp, bottom = 8.dp))
            Text("Export status: $exportStatus", modifier = Modifier.padding(bottom = 12.dp))

            Text("Suggested timeline", style = MaterialTheme.typography.titleMedium)
            LazyColumn(modifier = Modifier.fillMaxWidth()) {
                items(timeline) { clip ->
                    TimelineCard(clip)
                }
            }

            Text("Captions", style = MaterialTheme.typography.titleMedium, modifier = Modifier.padding(top = 12.dp))
            LazyColumn(modifier = Modifier.fillMaxWidth()) {
                items(captions) { caption ->
                    CaptionCard(caption)
                }
            }
        }
    }
}

@Composable
fun TimelineCard(clip: TimelineClip) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 6.dp)
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Text(clip.label)
            Text("${clip.start}s - ${clip.end}s")
            Text("confidence: ${clip.confidence}")
        }
    }
}

@Composable
fun CaptionCard(caption: CaptionItem) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 6.dp)
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Text(caption.timeRange)
            Text(caption.text)
        }
    }
}

data class TimelineClip(
    val id: String,
    val start: Float,
    val end: Float,
    val label: String,
    val confidence: Float
)

data class CaptionItem(
    val timeRange: String,
    val text: String
)

private fun persistProject(
    client: OkHttpClient,
    projectId: String,
    timeline: List<TimelineClip>,
    captions: List<CaptionItem>
) {
    val payload = """
        {
          "project_id": "$projectId",
          "timeline": [
            {"id":"clip-1","start":0.0,"end":3.0,"label":"intro","confidence":0.94},
            {"id":"clip-2","start":3.0,"end":8.0,"label":"highlight","confidence":0.91},
            {"id":"clip-3","start":8.0,"end":12.0,"label":"caption-shot","confidence":0.93}
          ],
          "captions": [
            {"start":0.0,"end":2.4,"text":"Welcome to Quicklab"},
            {"start":2.5,"end":5.0,"text":"AI-powered editing starts here"},
            {"start":5.1,"end":8.0,"text":"Create your next short in minutes"}
          ]
        }
    """.trimIndent()

    val request = Request.Builder()
        .url("http://10.0.2.2:8000/api/v1/projects/$projectId/persist")
        .post(payload.toRequestBody("application/json".toMediaTypeOrNull()))
        .build()

    Thread {
        client.newCall(request).execute().close()
    }.start()
}

private fun uploadVideo(
    client: OkHttpClient,
    projectId: String,
    uri: Uri,
    onResult: (String) -> Unit
) {
    val contentResolver = AppContextProvider.appContext.contentResolver
    val mimeType = contentResolver.getType(uri) ?: "video/mp4"
    val inputStream: InputStream = contentResolver.openInputStream(uri)
        ?: throw IllegalStateException("Could not open input stream")

    val bytes = inputStream.readBytes()
    val requestBody = bytes.toRequestBody(mimeType.toMediaTypeOrNull())

    val multipartBody = MultipartBody.Builder()
        .setType(MultipartBody.FORM)
        .addFormDataPart("file", "upload.mp4", requestBody)
        .build()

    val request = Request.Builder()
        .url("http://10.0.2.2:8000/api/v1/projects/$projectId/upload")
        .post(multipartBody)
        .build()

    Thread {
        try {
            val response = client.newCall(request).execute()
            val body = response.body?.string() ?: "No response body"
            onResult(body)
        } catch (e: Exception) {
            onResult("Upload failed: ${e.message}")
        }
    }.start()
}

private fun exportVideo(client: OkHttpClient, projectId: String, onResult: (String) -> Unit) {
    val payload = """
        {"project_id":"$projectId","format":"mp4","quality":"1080p"}
    """.trimIndent()

    val request = Request.Builder()
        .url("http://10.0.2.2:8000/api/v1/export")
        .post(payload.toRequestBody("application/json".toMediaTypeOrNull()))
        .build()

    Thread {
        try {
            val response = client.newCall(request).execute()
            val body = response.body?.string() ?: "No response body"
            onResult(body)
        } catch (e: Exception) {
            onResult("Export request failed: ${e.message}")
        }
    }.start()
}

object AppContextProvider {
    lateinit var appContext: android.content.Context
}
