using System;
using System.Collections.Generic;
using System.Windows.Forms;
using System.Data;
using System.IO;
using LiraAPI;
using FEModel;


namespace SettlementSheet
{
    public class SettlementSheetClass : ILiraAPI
    {
        ReturnCodes ILiraAPI.ExecuteProgram_Result(IResultLiraAPI result, int nodesNumber, int elementsNumber, List<List<Results_Key>> allLoadCases, Results_Key loadCase)
        {
            if (result.Equals(false))
            {
                MessageBox.Show("IResultLiraAPI return False\n" + ReturnCodes.RC_FAILED.ToString());

                return ReturnCodes.RC_FAILED;
            }

            List<int> elementArray = new List<int>(); //list with element numbers
            for (int i = 0; i < elementsNumber; i++)
            {
                elementArray.Add(i);
            }

            List<Results_Key> pKeyArr = new List<Results_Key> { loadCase }; //list of active design combination of loads            

            e_Results_ColumnType[] pColumnArr = null; //array with column type

            string[] pNameColumns = null; //array with column names

            DataTable allElements = result.get_TableResult(e_Results_TableType.RTT_ELEMENTS, elementArray, pKeyArr, ref pColumnArr, ref pNameColumns); //getting all elements
            DataTable allElementsBar = result.get_TableResult(e_Results_TableType.RTT_ELEMENTS_BAR_RSN_C, elementArray, allLoadCases[0], ref pColumnArr, ref pNameColumns); //getting efforts for the RSN

            string pathWriterCsv = Path.GetFullPath("SettlementSheet.csv"); //path to the file to write the results             

            using (StreamWriter file = new StreamWriter(pathWriterCsv, false))
            {
                file.Write("");
            }

            foreach (DataRow currentElement in allElements.Rows)
            {
                int numberElem = Convert.ToInt32(currentElement[0]);
                string construction = Convert.ToString(currentElement[6]).TrimStart(new char[] { ' ', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' });

                if (!String.IsNullOrEmpty(currentElement[6].ToString()))
                {
                    foreach (DataRow currentElementBar in allElementsBar.Rows)
                    {
                        int numberElemInBar = Convert.ToInt32(currentElementBar[0]);
                        double effort = Math.Round(Convert.ToSingle(currentElementBar[2]) * 0.000102, 3);

                        if (numberElemInBar == numberElem)
                        {
                            using (StreamWriter file = new StreamWriter(pathWriterCsv, true))
                            {
                                string tableOutput = $"{numberElem},{construction},{effort}";

                                file.WriteLine(tableOutput);
                            }
                        }
                    }
                }
            }

            MessageBox.Show("Расчет успешно выполнен!");

            return ReturnCodes.RC_OK;
        }

    }
}
