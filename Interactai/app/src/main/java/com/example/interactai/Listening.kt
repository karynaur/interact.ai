package com.example.interactai

//class Listening : AppCompatActivity() {
//    override fun onCreate(savedInstanceState: Bundle?) {
//        super.onCreate(savedInstanceState)
//        setContentView(R.layout.activity_listening)
//    }
//}
import android.view.View
import android.content.Intent
import android.graphics.PointF.length
import android.widget.VideoView
import androidx.appcompat.app.AppCompatActivity
import android.net.Uri
import android.os.Bundle
import android.speech.RecognizerIntent
import android.util.Log
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import com.bumptech.glide.Glide
import com.google.gson.JsonArray
import com.koushikdutta.ion.Ion
import org.json.JSONArray
import org.json.JSONObject
import java.net.URL
import java.util.*
import kotlin.concurrent.schedule
import kotlin.concurrent.timerTask

class Listening : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_listening)
        //configureVideoView()
        //showGif()
        findViewById<TextView>(R.id.display).text = "Input text : "

    }

    private fun flaskCall(req: String) {

        lateinit var webView: WebView
        webView = findViewById(R.id.webView)
        webView.settings.setJavaScriptEnabled(true)

        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(view: WebView?, url: String?): Boolean {
                if (url != null) {
                    view?.loadUrl(url)
                }
                return true
            }
        }
        val rer = req.replace(" ", "+")
        Log.d("vish", rer)
        webView.loadUrl("http://192.168.0.106:5000/get/" + rer)
        Toast.makeText(this, "delay of 15", Toast.LENGTH_SHORT)
        Log.d("vish", "delay of 15")
        Thread.sleep(20000)

        Ion.with(this)
                .load("http://192.168.0.106:80/output.html")
                .asString()
                .setCallback{ _ , result ->
                    Log.d("vish", "JSON IS $result")
                    configureVideoView(result)
                }
    }

    fun connectVideo(view: View) {
        Toast.makeText(applicationContext, "Speak now to send your message.", Toast.LENGTH_SHORT).show()

        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault())
        if (intent.resolveActivity(packageManager) != null) {
            startActivityForResult(intent, 10)
        } else {
            Toast.makeText(applicationContext, "Your device does not support speech recognition", Toast.LENGTH_SHORT).show()
            Log.e("err", "errrrorrr")
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        when (requestCode) {
            10 -> if (resultCode == RESULT_OK && data != null) {
                val result: ArrayList<String> = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS) as ArrayList<String>
                val final = "Input text : \n" + result.get(0)
                findViewById<TextView>(R.id.display).text = final
                Log.d("vish", "$final")
                flaskCall(result[0])
                // pass $result to the server
            }
        }
    }
    private fun configureVideoView(result:String) {

        val vid = findViewById<VideoView>(R.id.videoView) // as VideoView
        //make a loop here to display word by word videos and GIFs
//        {
//            "files" :
//            [
//                {
//                    "word":{"0":21,"1":21,"2":42,"3":42},
//                    "length":0.234
//                }
//                {
//                    "word":{"0":21,"1":21,"2":42,"3":42},
//                    "length":0.234
//                }
//            ]
//        }
        val files = JSONObject("{\"files\":$result}")
        val array = files.getJSONArray("files")
        val word = array.getJSONObject(0)
        val number = word.getJSONObject("word")
        val length = word.getLong("length")

        vid.setVideoPath("http://192.168.0.106:80/videos/0.mp4")
        vid.start()

        for (i in 0 until number.length()) {
            var num = number.getString("$i")
            Thread.sleep(length)
            showGif(i)
            Log.d("vish", "$i is $num")
        }

    }

    fun showGif(i:Int) {
        val imageView = findViewById<ImageView>(R.id.imageView)
        // make a loop here and add the delays to show gifs (hand positions)
        var z = "R.drawable.h$i"
        Log.d("vish", z)
        Glide.with(this).load(R.drawable.h21).into(imageView)  //edit tenor to the files downloaded
    }
}
