using System;
using System.Text;
using System.Data;
using System.Data.SQLite;

namespace airo_heat_tool.Models
{
    public class Data
    {
        private SQLiteConnection sqlite;

        public Data()
        {
              sqlite = new SQLiteConnection("Data Source=/home/mimi/airo-heat-tool/database.db;New=False;");

        }


         public DataTable selectQuery(string query)
        {
            SQLiteDataAdapter ad;
            DataTable dataTable = new DataTable();
            var dataSet = new DataSet();

              try
              {
                    SQLiteCommand cmd;
                    sqlite.Open();  //Initiate connection to the db
                    cmd = sqlite.CreateCommand();
                    cmd.CommandText = query;  //set the passed query
                    ad = new SQLiteDataAdapter(cmd);
                    ad.Fill(dataSet, "AP"); //fill the datasource
                    dataTable=dataSet.Tables["AP"];
              }
              catch(SQLiteException ex)
              {
                  Console.WriteLine(ex.Message);
              }
            sqlite.Close();
            return dataTable;
        }
    }
}