package com.example.facerecognition;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Base64;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.ByteArrayOutputStream;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {

    private ImageView imageView;
    private Button capture;
    private Button predict;
    private TextView text;

    private Bitmap bitmap;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        imageView=findViewById(R.id.imageView);
        capture=findViewById(R.id.capture_button);
        predict=findViewById(R.id.predict_button);
        text=findViewById(R.id.text);

        capture.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                ImageCapture();
            }
        });

        predict.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Predict();
            }
        });
    }

    private void ImageCapture(){
        Intent intent=new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        startActivityForResult(intent,0);
    }
    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if(requestCode==0 && resultCode==RESULT_OK && data!=null){
            bitmap=(Bitmap)data.getExtras().get("data");
            imageView.setImageBitmap(bitmap);
            Toast.makeText(MainActivity.this,"Image Captured",Toast.LENGTH_SHORT).show();
        }
    }

    private void Predict(){
        String image=imageToString();
        ApiInterface apiInterface=ApiClient.getApiClient().create(ApiInterface.class);
        Call<ImageClass> call=apiInterface.uploadImage(image);
        call.enqueue(new Callback<ImageClass>() {
            @Override
            public void onResponse(Call<ImageClass> call, Response<ImageClass> response) {
                ImageClass imageClass=response.body();
                text.setText(imageClass.getCaption());
                //Toast.makeText(MainActivity.this,"Server Response: "+imageClass.getCaption(),Toast.LENGTH_LONG).show();
            }

            @Override
            public void onFailure(Call<ImageClass> call, Throwable t) {
                Toast.makeText(getApplicationContext(),t.getMessage(),Toast.LENGTH_LONG).show();
            }
        });
    }
    private String imageToString(){
        ByteArrayOutputStream byteArrayOutputStream=new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.JPEG,100,byteArrayOutputStream);
        byte[] imgByte=byteArrayOutputStream.toByteArray();
        return Base64.encodeToString(imgByte,Base64.DEFAULT);
    }
}
