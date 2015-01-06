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
import android.widget.ToggleButton;

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
    public int user_m1;
    public int user_m2;
    public int mute_m1;
    public int mute_m2;
    public int debug_mode;
    public int auto_mode;
    public int shutdown;


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

    //socket portion
    private PrintWriter printwriter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sound);

        //seekbar
        SeekBar freqsb = (SeekBar) findViewById(R.id.freqBar);
        SeekBar phasesb = (SeekBar) findViewById(R.id.phaseBar);
        SeekBar m1sb = (SeekBar) findViewById(R.id.m1bar);
        SeekBar m2sb = (SeekBar) findViewById(R.id.m2bar);

        //switch
        Switch autoSwitch = (Switch) findViewById(R.id.switchAuto);

        //button
        Button dbgButton = (Button) findViewById(R.id.debug_button);
        ToggleButton m1Toggle = (ToggleButton) findViewById(R.id.m1Toggle);
        ToggleButton m2Toggle = (ToggleButton) findViewById(R.id.m2Toggle);
        Button shutDownButton = (Button) findViewById(R.id.btnStop);

        //static
        final EditText ipAddr = (EditText) findViewById(R.id.ipAddr);

        //set initial positions
        m1sb.setProgress(300);
        m2sb.setProgress(300);

        //for now set auto_mode and debug_mode to be false
        synchronized(SharedData.globalInstance) {
            SharedData.globalInstance.debug_mode = 0;
            SharedData.globalInstance.auto_mode = 0;
            SharedData.globalInstance.user_freq = 200;
            SharedData.globalInstance.user_phase = 0;
            SharedData.globalInstance.user_m1 = 300;
            SharedData.globalInstance.user_m2 = 300;
            SharedData.globalInstance.mute_m1 = 0;
            SharedData.globalInstance.mute_m2 = 0;
            SharedData.globalInstance.shutdown = 0;
            SharedData.globalInstance.s_address = "127.0.0.1";
            SharedData.globalInstance.s_port = 9999;
            SharedData.globalInstance.new_in = false;
            SharedData.globalInstance.connected = false;
        }

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

        dbgButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                // Perform action on click
                synchronized (SharedData.globalInstance) {
                    SharedData.globalInstance.debug_mode = 1;
                    SharedData.globalInstance.s_address = ipAddr.getText().toString();
                    SharedData.globalInstance.new_in = true;
                }
            }
        });

        shutDownButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                synchronized (SharedData.globalInstance) {
                    SharedData.globalInstance.shutdown = 1;
                    SharedData.globalInstance.new_in = true;
                }
            }
        });

        autoSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked) {
                    // The toggle is enabled
                    synchronized (SharedData.globalInstance) {
                        SharedData.globalInstance.auto_mode = 1;
                        SharedData.globalInstance.new_in = true;
                    }
                } else {
                    // The toggle is disabled
                    synchronized (SharedData.globalInstance) {
                        SharedData.globalInstance.auto_mode = 0;
                        SharedData.globalInstance.new_in = true;
                    }
                }
            }
        });

        //Magnitude 1
        m1sb.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            TextView text_label = (TextView) findViewById(R.id.textView);

            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                text_label.setText(""+progress);
                synchronized (SharedData.globalInstance) {
                    SharedData.globalInstance.user_m1 = progress;
                    SharedData.globalInstance.new_in = true;
                }
            }
            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {}
            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {}
        });

        //Magnitude 2
        m2sb.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {

            TextView text_label = (TextView) findViewById(R.id.textView2);

            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                text_label.setText(""+progress);
                synchronized (SharedData.globalInstance) {
                    SharedData.globalInstance.user_m2 = progress;
                    SharedData.globalInstance.new_in = true;
                }
            }
            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {}
            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {}
        });

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
            public void onStartTrackingTouch(SeekBar seekBar) {}
            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {}
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
            public void onStartTrackingTouch(SeekBar seekBar) {}
            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {}
        });

        m1Toggle.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked) {
                    // The toggle is enabled
                    synchronized (SharedData.globalInstance) {
                        SharedData.globalInstance.mute_m1 = 1;
                        SharedData.globalInstance.new_in = true;
                    }
                } else {
                    // The toggle is disabled
                    synchronized (SharedData.globalInstance) {
                        SharedData.globalInstance.mute_m1 = 0;
                        SharedData.globalInstance.new_in = true;
                    }
                }
            }
        });

        m2Toggle.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked) {
                    // The toggle is enabled
                    synchronized (SharedData.globalInstance) {
                        SharedData.globalInstance.mute_m2 = 1;
                        SharedData.globalInstance.new_in = true;
                    }
                } else {
                    // The toggle is disabled
                    synchronized (SharedData.globalInstance) {
                        SharedData.globalInstance.mute_m2 = 0;
                        SharedData.globalInstance.new_in = true;
                    }
                }
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
            int r_auto_mode;
            int r_mag1;
            int r_mag2;
            int r_mute1;
            int r_mute2;
            int shutdown;
            int dbgMode;

            synchronized (SharedData.globalInstance) {
                r_user_freq = SharedData.globalInstance.user_freq;
                r_user_phase = SharedData.globalInstance.user_phase;
                r_auto_mode = SharedData.globalInstance.auto_mode;
                r_mag1 = SharedData.globalInstance.user_m1;
                r_mag2 = SharedData.globalInstance.user_m2;
                r_mute1 = SharedData.globalInstance.mute_m1;
                r_mute2 = SharedData.globalInstance.mute_m2;
                shutdown = SharedData.globalInstance.shutdown;
                dbgMode = SharedData.globalInstance.debug_mode;

                SharedData.globalInstance.debug_mode = 0;
            }

            //assemble JSON object
            JSONObject message = new JSONObject();
            try {
                message.put("freq", r_user_freq);
                message.put("phase", r_user_phase);
                message.put("auto", r_auto_mode);
                message.put("debug", dbgMode);
                message.put("mag1", r_mag1);
                message.put("mag2", r_mag2);
                message.put("mute1", r_mute1);
                message.put("mute2", r_mute2);
                message.put("shutdown", shutdown);
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
