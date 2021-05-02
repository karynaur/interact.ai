package com.example.interactai

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.util.Log
import com.koushikdutta.ion.Ion
import android.view.View
import android.widget.ImageView
import android.widget.VideoView
import androidx.appcompat.app.AppCompatActivity
import com.bumptech.glide.Glide
import org.json.JSONArray
import org.json.JSONObject

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }

    fun listen_intent(view: View){
        val intent = Intent(this, Listening::class.java)
        startActivity(intent)
    }
}