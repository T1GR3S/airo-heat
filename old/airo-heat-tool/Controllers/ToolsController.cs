using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using airo_heat_tool.Models;
using System.Data;
using Newtonsoft.Json;

namespace airo_heat_tool.Controllers
{
    public class ToolsController : Controller
    {
        public IActionResult Index()
        {
                      
            return View();
        }

        public IActionResult HeatMap()
        {
             ViewData["Title"] = "HeatMap";
             ViewData["Message"] = "HeatMap en desarrollo... v.100";

            
            Data pruebaBBDD = new Data();
            DataTable myData = pruebaBBDD.selectQuery("SELECT bssid, lat, lon, signal_rssi FROM SeenAp");
            HeatMap customHeatMap = new HeatMap();

            foreach (DataRow row in myData.Rows){
                customHeatMap.seenAPs.Add(new AccessPoint(row["bssid"].ToString(), row["lat"].ToString(), row["lon"].ToString(), row["signal_rssi"].ToString()));
            }
        
            return View(customHeatMap);
        }
        
    }
}
