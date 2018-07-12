package com.valleapp.valletpv.db;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteException;
import android.database.sqlite.SQLiteOpenHelper;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;


/**
 * Created by valle on 13/10/14.
 */
public class DbAccesos extends SQLiteOpenHelper {

    // If you change the database schema, you must increment the database version.
    public static final int DATABASE_VERSION = 1;
    public static final String DATABASE_NAME = "valletpv";


    public DbAccesos(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    public void onCreate(SQLiteDatabase db) {
        db.execSQL("CREATE TABLE IF NOT EXISTS sync (ID INTEGER PRIMARY KEY, Hora TEXT)");
    }

    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        // This database is only a cache for online data, so its upgrade policy is
        // to simply to discard the data and start over
        db.execSQL("DROP TABLE IF EXISTS sync");
        onCreate(db);
    }

    public void onDowngrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        onUpgrade(db, oldVersion, newVersion);
    }


    public void addAcceso(String hora){
        // Gets the data repository in write mode
        SQLiteDatabase db = this.getWritableDatabase();
        try{
           db.execSQL("DELETE FROM sync");
        }catch (SQLiteException e){
            this.onCreate(db);
        }
        // Insert the new row, returning the primary key value of the new row
         ContentValues values = new ContentValues();
         values.put("ID", 0);
         values.put("Hora", hora);
         db.insert("sync", null, values);
         db.close();
    }

    public String getUltimoAcceso()
    {
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor =  db.rawQuery( "select * from sync", null );
        String hora = "";
        cursor.moveToFirst();
        if (cursor.getCount() > 0 && cursor.getColumnCount() > 0) {
            hora = cursor.getString(cursor.getColumnIndex("Hora"));
        }
        cursor.close();
        db.close();
        return hora;

    }


    public int getCount() {
        SQLiteDatabase db = this.getReadableDatabase();
        int salida = 0;
        Cursor cursor = db.rawQuery("select count(*) from sync", null);
        cursor.moveToFirst();
        if (cursor.getCount() > 0 && cursor.getColumnCount() > 0) {
            salida = cursor.getInt(0);
            cursor.close();db.close();
            return salida;
        }
        cursor.close();db.close();
        return salida;

    }

    public void Vaciar(){
        SQLiteDatabase db = this.getWritableDatabase();
        try {
           db.execSQL("DELETE FROM sync");
        }catch (SQLiteException e) {
            db.execSQL("CREATE TABLE  sync (ID INTEGER, Hora TEXT)");
        }

        db.close();
    }

    /**
     * Created by valle on 13/10/14.
     */
    public static class DbSecciones extends SQLiteOpenHelper {

        // If you change the database schema, you must increment the database version.
        public static final int DATABASE_VERSION = 1;
        public static final String DATABASE_NAME = "valleptv";


        public DbSecciones(Context context) {
            super(context, DATABASE_NAME, null, DATABASE_VERSION);
        }

        public void onCreate(SQLiteDatabase db) {
            db.execSQL("CREATE TABLE  secciones (ID INTEGER, Nombre TEXT, RGB TEXT)");
        }

        public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
            // This database is only a cache for online data, so its upgrade policy is
            // to simply to discard the data and start over
            db.execSQL("DROP TABLE IF EXISTS secciones");
            onCreate(db);
        }

        public void onDowngrade(SQLiteDatabase db, int oldVersion, int newVersion) {
            onUpgrade(db, oldVersion, newVersion);
        }


        public void RellenarTabla(JSONArray datos){
            // Gets the data repository in write mode
            SQLiteDatabase db = this.getWritableDatabase();
            try {
               db.execSQL("DELETE FROM secciones");
            }catch (SQLiteException e){
                this.onCreate(db);
            }
           // Insert the new row, returning the primary key value of the new row
            for (int i= 0 ; i<datos.length();i++){
                // Create a new map of values, where column names are the keys
                try {
                     ContentValues values = new ContentValues();
                     values.put("ID", datos.getJSONObject(i).getInt("ID"));
                     values.put("Nombre", datos.getJSONObject(i).getString("Nombre"));
                     values.put("RGB", datos.getJSONObject(i).getString("RGB"));
                     db.insert("secciones", null, values);
                } catch (JSONException e) {
                    e.printStackTrace();
                }

            }
            db.close();
        }

        public JSONArray getAll()
        {
            JSONArray ls = new JSONArray();
            SQLiteDatabase db = this.getReadableDatabase();
            Cursor res =  db.rawQuery( "select * from secciones", null );
            res.moveToFirst();
            while(res.isAfterLast() == false){
                try{
                    JSONObject obj = new JSONObject();
                    obj.put("Nombre", res.getString(res.getColumnIndex("Nombre")));
                    obj.put("ID", res.getString(res.getColumnIndex("ID")));
                    obj.put("RGB", res.getString(res.getColumnIndex("RGB")));
                    ls.put(obj);
                } catch (JSONException e) {
                    e.printStackTrace();
                }

                res.moveToNext();

            }
            res.close();db.close();
            return ls;
        }


        public int getCount() {
            SQLiteDatabase db = this.getReadableDatabase();
            int s = 0;
            Cursor cursor = db.rawQuery("select count(*) from secciones", null);
            cursor.moveToFirst();
            if (cursor.getCount() > 0 && cursor.getColumnCount() > 0) {
                s = cursor.getInt(0);
            }
                cursor.close();db.close();
                return  s;
        }

        public void Vaciar(){
            SQLiteDatabase db = this.getWritableDatabase();
            try{
              db.execSQL("DELETE FROM secciones");
            }catch (SQLiteException e){
                this.onCreate(db);
            }
            db.close();
        }
    }
}
