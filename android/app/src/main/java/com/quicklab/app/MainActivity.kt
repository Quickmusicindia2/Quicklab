package com.quicklab.app

import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
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

    val launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent(),
        onResult = { uri ->
            if (uri != null) {
                selectedFileName = uri.lastPathSegment ?: "selected_video.mp4"
                uploadVideo(client, uri, onResult = { responseText ->
                    resultText = responseText
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
                .padding(24.dp),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text("Quicklab")
            Text("AI video editor")
            Text("Selected: $selectedFileName")

            Button(onClick = { launcher.launch("video/*") }) {
                Text("Pick Video")
            }

            Text(resultText)
        }
    }
}

private fun uploadVideo(
    client: OkHttpClient,
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
        .url("http://10.0.2.2:8000/api/v1/projects/proj-0001/upload")
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

object AppContextProvider {
    lateinit var appContext: android.content.Context
}
