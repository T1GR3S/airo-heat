using System;

namespace airo_heat_tool.Models
{
    public class AccessPoint
    {
        public string bssid {get; set;}
        public string lat {get; set;}
        public string lon {get; set;}
        public string rssi {get; set;}

        public AccessPoint (string new_bssid, string new_lat, string new_lon, string new_rssi){
            bssid = new_bssid;
            lat = new_lat;
            lon = new_lon;
            rssi = new_rssi;
        } 
    }
}