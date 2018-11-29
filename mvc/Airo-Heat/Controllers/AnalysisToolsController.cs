using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Airo_Heat.Models;

namespace Airo_Heat.Controllers
{
     public class AnalysisToolsController : Controller
    {
        public IActionResult Index()
        {

            ViewData["Title"] = "Statistics";

            ViewData["Message"] = "Pagina de estadisticas";

            return View();
        }
    }
}