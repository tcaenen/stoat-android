package chat.stoat

import android.app.Application
import android.os.Build
import android.os.StrictMode
import com.google.android.material.color.DynamicColors
import dagger.hilt.android.HiltAndroidApp
import logcat.AndroidLogcatLogger
import logcat.LogPriority

import chat.stoat.persistence.KVStorage
import kotlinx.coroutines.runBlocking
import javax.inject.Inject

@HiltAndroidApp
class StoatApplication : Application() {
    companion object {
        lateinit var instance: StoatApplication
    }

    @Inject
    lateinit var kvStorage: KVStorage

    override fun onCreate() {
        super.onCreate()
        AndroidLogcatLogger.installOnDebuggableApp(this, minPriority = LogPriority.VERBOSE)

        runBlocking {
            val savedUrl = kvStorage.get("instance_url")
            if (savedUrl != null) {
                chat.stoat.api.configureStoatUrls(savedUrl)
            }
        }

        if (BuildConfig.DEBUG) {
            // Enable strict mode primarily to catch non-API usage, although we detect all
            // violations for our reference.
            // https://developer.android.com/reference/android/os/StrictMode
            StrictMode.setVmPolicy(
                StrictMode.VmPolicy
                    .Builder()
                    .apply {
                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                            detectNonSdkApiUsage()
                        }
                        penaltyLog()
                    }
                    .build()
            )
        }
    }

    init {
        instance = this
        DynamicColors.applyToActivitiesIfAvailable(this)
    }
}
