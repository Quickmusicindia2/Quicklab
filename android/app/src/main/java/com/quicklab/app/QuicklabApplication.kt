package com.quicklab.app

import android.app.Application

class QuicklabApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        AppContextProvider.appContext = this
    }
}
