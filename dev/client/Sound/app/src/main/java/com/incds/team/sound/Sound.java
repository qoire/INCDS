package com.incds.team.sound;

import android.media.AudioFormat;
import android.media.AudioRecord;
import android.media.MediaRecorder;
import android.os.AsyncTask;
import android.os.Environment;
import android.os.Handler;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.SeekBar;
import android.widget.Switch;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Timer;
import java.util.TimerTask;

class SharedData {
    public int user_freq;
    public int user_phase;
    public String debug_mode;
    public String auto_mode;

    //necessary for function
    public String s_address;
    public int s_port;
    public Boolean new_in;
    public Boolean connected;
    public static SharedData globalInstance = new SharedData();
}

public class Sound extends ActionBarActivity {

    public static String audio_file;
    private Timer timer;

    private static final String TAG = "com.incds.team.sound";

    //audio portion
    private static final String AUDIO_RECORDER_FILE_EXT_WAV = ".wav";
    private static final String AUDIO_RECORDER_FOLDER = "AudioRecorder";
    private static final String AUDIO_RECORDER_TEMP_FILE = "record_temp.raw";

    private static final int RECORDER_BPP = 16;
    private static final int RECORDER_SAMPLERATE = 44100;
    private static final int RECORDER_CHANNELS = AudioFormat.CHANNEL_IN_MONO;
    private static final int RECORDER_AUDIO_ENCODING = AudioFormat.ENCODING_PCM_16BIT;
    private static int BUFFER_SIZE = AudioRecord.getMinBufferSize(RECORDER_SAMPLERATE, RECORDER_CHANNELS,
            RECORDER_AUDIO_ENCODING);
    private AudioRecord recorder = null;
    private boolean isRecording = false;
    private Thread recordingThread = null;

    //socket portion
    private PrintWriter printwriter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sound);

        SeekBar freqsb = (SeekBar) findViewById(R.id.freqBar);
        SeekBar phasesb = (SeekBar) findViewById(R.id.phaseBar);
        Button dbgButton = (Button) findViewById(R.id.debug_button);
        Switch autoSwitch = (Switch) findViewById(R.id.switchAuto);
        final EditText ipAddr = (EditText) findViewById(R.id.ipAddr);

        //for now set auto_mode and debug_mode to be false
        synchronized(SharedData.globalInstance) {
            SharedData.globalInstance.debug_mode = "False";
            SharedData.globalInstance.auto_mode = "False";
            SharedData.globalInstance.user_freq = 200;
            SharedData.globalInstance.user_phase = 0;
            SharedData.globalInstance.s_address = "192.168.10.101";
            SharedData.globalInstance.s_port = 9999;
            SharedData.globalInstance.new_in = false;
            SharedData.globalInstance.connected = false;
        }

        dbgButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                // Perform action on click
                synchronized (SharedData.globalInstance) {
                    SharedData.globalInstance.debug_mode = "True";
                    SharedData.globalInstance.new_in = true;
                    SharedData.globalInstance.s_address = ipAddr.getText().toString();
                }
            }
        });

        autoSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked) {
                    // The toggle is enabled
                    synchronized (SharedData.globalInstance) {
                        SharedData.globalInstance.auto_mode = "True";
                        SharedData.globalInstance.new_in = true;
                    }
                } else {
                    // The toggle is disabled
                    synchronized (SharedData.globalInstance) {
                        SharedData.globalInstance.auto_mode = "False";
                        SharedData.globalInstance.new_in = true;
                    }
                }
            }
        });

        //create thread for handling
        Thread messageThread = new Thread(new Runnable() {
            @Override
            public void run() {
                while (true) {
                    Boolean run_necessary;
                    String addr;
                    int port;

                    synchronized (SharedData.globalInstance) {
                        run_necessary = SharedData.globalInstance.new_in;
                        addr = SharedData.globalInstance.s_address;
                        port = SharedData.globalInstance.s_port;
                    }

                    if (addr == "127.0.0.1") {
                        try {
                            Thread.sleep(50);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                        continue;
                    }

                    if (run_necessary) {
                        messageClient m_client = new messageClient(addr, port);
                        m_client.execute();

                        //message sent
                        synchronized(SharedData.globalInstance) {
                            SharedData.globalInstance.new_in = false;
                        }
                    }

                    //sleep the thread to reduce CPU usage
                    try {
                        Thread.sleep(50);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        });
        messageThread.start();

        //Set Listener for Freq
        freqsb.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            TextView freqtext = (TextView) findViewById(R.id.textFrequency);
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                int hertz = progress + 200;
                freqtext.setText(""+hertz+" Hz");

                synchronized (SharedData.globalInstance) {
                    SharedData.globalInstance.user_freq = hertz;
                    SharedData.globalInstance.new_in = true;
                }
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

        //Set Listener for Phase
        phasesb.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {

            TextView phasetext = (TextView) findViewById(R.id.textPhase);

            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                int phase = progress;
                phasetext.setText(""+phase+" °");

                synchronized (SharedData.globalInstance) {
                    SharedData.globalInstance.user_phase = phase;
                    SharedData.globalInstance.new_in = true;
                }
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_sound, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    //AUDIO HANDLING
    public void callAudioTask() {
        Timer timer = new Timer();
        TimerTask asyncAudioTask = new TimerTask() {

            @Override
            public void run() {
                Timer wait_timer = new Timer();
                TimerTask stopAudio = new TimerTask() {
                    @Override
                    public void run() {
                        stopRecording();
                    }
                };
                wait_timer.schedule(stopAudio, 300);
                callAudio();
            }
        };
        timer.schedule(asyncAudioTask, 0, 500);
    }

    private void callAudio() {
        recorder = new AudioRecord(MediaRecorder.AudioSource.MIC,
                RECORDER_SAMPLERATE, RECORDER_CHANNELS, RECORDER_AUDIO_ENCODING,
                BUFFER_SIZE);
        int i = recorder.getState();
        if (i==1)
            recorder.startRecording();
        isRecording = true;

        //create thread for writing audio data
        Thread recordingThread = new Thread(new Runnable() {
            @Override
            public void run() {

                byte data[] = new byte[BUFFER_SIZE];

                FileOutputStream os = null;

                try {
                    os = new FileOutputStream(getTempFilename());
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                }

                int read = 0;

                if (os != null) {
                    while (isRecording) {
                        read = recorder.read(data, 0, BUFFER_SIZE);
                        if (read > 0) {
                            try {
                                os.write(data);
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                        }
                        else if (read == AudioRecord.ERROR_INVALID_OPERATION) {
                            Log.e("Recording", "Invalid operation error");
                            break;
                        }
                        else if (read == AudioRecord.ERROR_BAD_VALUE) {
                            Log.e("Recording", "Bad value error");
                            break;
                        }
                        else if (read == AudioRecord.ERROR) {
                            Log.e("Recording", "Unknown Error");
                            break;
                        }

                        //sleep
                        try {
                            Thread.sleep(10);
                        } catch (InterruptedException e) {
                            break;
                        }
                    }
                }
            }
        });
        recordingThread.start();
    }

    private String getFilename(){
        String filepath = Environment.getExternalStorageDirectory().getPath();
        File file = new File(filepath,AUDIO_RECORDER_FOLDER);

        if(!file.exists()){
            file.mkdirs();
        }
        return (file.getAbsolutePath() + "/" + System.currentTimeMillis() + AUDIO_RECORDER_FILE_EXT_WAV);
    }

    private String getTempFilename(){
        String filepath = Environment.getExternalStorageDirectory().getPath();
        File file = new File(filepath,AUDIO_RECORDER_FOLDER);

        if(!file.exists()){
            file.mkdirs();
        }

        File tempFile = new File(filepath,AUDIO_RECORDER_TEMP_FILE);

        if(tempFile.exists())
            tempFile.delete();

        return (file.getAbsolutePath() + "/" + AUDIO_RECORDER_TEMP_FILE);
    }
    private void stopRecording() {
        if (recorder != null) {
            isRecording = false;
            int i = recorder.getState();
            if (i==1)
                recorder.stop();
            recorder.release();
            recorder = null;
            recordingThread = null;
        }
        copyWaveFile(getTempFilename(),getFilename());
        deleteTempFile();
    }

    private void deleteTempFile() {
        File file = new File(getTempFilename());

        file.delete();
    }

    private void copyWaveFile(String inFilename,String outFilename){
        FileInputStream in = null;
        FileOutputStream out = null;
        long totalAudioLen = 0;
        long totalDataLen = totalAudioLen + 36;
        long longSampleRate = RECORDER_SAMPLERATE;
        int channels = 1;
        long byteRate = RECORDER_BPP * RECORDER_SAMPLERATE * channels/8;

        byte[] data = new byte[BUFFER_SIZE];

        try {
            in = new FileInputStream(inFilename);
            out = new FileOutputStream(outFilename);
            totalAudioLen = in.getChannel().size();
            totalDataLen = totalAudioLen + 36;

            // AppLog.logString("File size: " + totalDataLen);

            WriteWaveFileHeader(out, totalAudioLen, totalDataLen,
                    longSampleRate, channels, byteRate);

            while(in.read(data) != -1){
                out.write(data);
            }

            in.close();
            out.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void WriteWaveFileHeader(
            FileOutputStream out, long totalAudioLen,
            long totalDataLen, long longSampleRate, int channels,
            long byteRate) throws IOException {

        byte[] header = new byte[44];

        header[0] = 'R';  // RIFF/WAVE header
        header[1] = 'I';
        header[2] = 'F';
        header[3] = 'F';
        header[4] = (byte) (totalDataLen & 0xff);
        header[5] = (byte) ((totalDataLen >> 8) & 0xff);
        header[6] = (byte) ((totalDataLen >> 16) & 0xff);
        header[7] = (byte) ((totalDataLen >> 24) & 0xff);
        header[8] = 'W';
        header[9] = 'A';
        header[10] = 'V';
        header[11] = 'E';
        header[12] = 'f';  // 'fmt ' chunk
        header[13] = 'm';
        header[14] = 't';
        header[15] = ' ';
        header[16] = 16;  // 4 bytes: size of 'fmt ' chunk
        header[17] = 0;
        header[18] = 0;
        header[19] = 0;
        header[20] = 1;  // format = 1
        header[21] = 0;
        header[22] = (byte) channels;
        header[23] = 0;
        header[24] = (byte) (longSampleRate & 0xff);
        header[25] = (byte) ((longSampleRate >> 8) & 0xff);
        header[26] = (byte) ((longSampleRate >> 16) & 0xff);
        header[27] = (byte) ((longSampleRate >> 24) & 0xff);
        header[28] = (byte) (byteRate & 0xff);
        header[29] = (byte) ((byteRate >> 8) & 0xff);
        header[30] = (byte) ((byteRate >> 16) & 0xff);
        header[31] = (byte) ((byteRate >> 24) & 0xff);
        header[32] = (byte) (2 * 16 / 8);  // block align
        header[33] = 0;
        header[34] = RECORDER_BPP;  // bits per sample
        header[35] = 0;
        header[36] = 'd';
        header[37] = 'a';
        header[38] = 't';
        header[39] = 'a';
        header[40] = (byte) (totalAudioLen & 0xff);
        header[41] = (byte) ((totalAudioLen >> 8) & 0xff);
        header[42] = (byte) ((totalAudioLen >> 16) & 0xff);
        header[43] = (byte) ((totalAudioLen >> 24) & 0xff);

        out.write(header, 0, 44);
    }

    //delete all files from previous sessions
    private void cleanUp() {
        String filepath = Environment.getExternalStorageDirectory().getPath();
        File file = new File(filepath,AUDIO_RECORDER_FOLDER);

        if (file.isDirectory()) {
            String[] children = file.list();
            for (int i = 0; i < children.length; i++) {
                new File(file, children[i]).delete();
            }
        }
    }

    //async method for handling socket
    public class messageClient extends AsyncTask<Void, Void, Void> {
        String dstAddress;
        int dstPort;

        messageClient(String addr, int port) {
            dstAddress = addr;
            dstPort = port;
        }

        @Override
        protected Void doInBackground(Void... arg0) {
            Socket socket = null;
            int r_user_freq;
            int r_user_phase;
            String r_auto_mode;
            String dbgMode;

            synchronized (SharedData.globalInstance) {
                r_user_freq = SharedData.globalInstance.user_freq;
                r_user_phase = SharedData.globalInstance.user_phase;
                r_auto_mode = SharedData.globalInstance.auto_mode;
                dbgMode = SharedData.globalInstance.debug_mode;
                SharedData.globalInstance.debug_mode = "False";
            }

            //assemble JSON object
            JSONObject message = new JSONObject();
            try {
                message.put("freq", r_user_freq);
                message.put("phase", r_user_phase);
                message.put("auto", r_auto_mode);
                message.put("debug", dbgMode);
            } catch(JSONException e) {
                e.printStackTrace();
            }

            try {
                socket = new Socket(dstAddress, dstPort);
                printwriter = new PrintWriter(socket.getOutputStream(), true);
                printwriter.write(message.toString() + '\n');
                printwriter.flush();
                printwriter.close();
                socket.close();
            } catch(UnknownHostException e) {
                e.printStackTrace();
            } catch(IOException e) {
                e.printStackTrace();
            }

            return null;
        }
    }
}
