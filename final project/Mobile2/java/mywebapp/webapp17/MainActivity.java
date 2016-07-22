import android.annotation.SuppressLint;
import android.app.Activity;
import android.os.Bundle;
import android.webkit.GeolocationPermissions;
import android.webkit.WebChromeClient;
import android.webkit.WebView;

import mywebapp.webapp17.R;

public class MainActivity extends Activity {
    private static final String URL = "https://vlaskin-assignment2.appspot.com";
    private WebView webview;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        webview = (WebView) findViewById(R.id.webView);
        webview.getSettings().setJavaScriptEnabled(true);
        webview.getSettings().setDomStorageEnabled(true);
        webview.getSettings().setGeolocationEnabled(true);
        webview.getSettings().setDefaultTextEncodingName("utf-8");
        webview.getSettings().setJavaScriptCanOpenWindowsAutomatically(true);
        webview.setWebChromeClient(new GeoWebChromeClient());
        webview.loadUrl(URL);

    }
    @Override
    public class GeoWebChromeClient extends WebChromeClient {
        public void onGeolocationPermissionsShowPrompt(String origin, GeolocationPermissions.Callback callback){
            callback.invoke(origin, true, false);
        }
    }

    public void onGeolocationPermissionsShowPrompt(String origin, android.webkit.GeolocationPermissions.Callback callback) {
        callback.invoke(origin, true, false);
    }

}
