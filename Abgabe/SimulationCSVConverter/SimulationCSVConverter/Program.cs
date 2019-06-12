using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using SimulationCSVConverter.Functions;
using SimulationCSVConverter.Objects;

namespace SimulationCSVConverter
{
    public class Program
    {
        private const int Interval = 1000;
        private const bool UseShortNotationForm = true;
        private const bool OnlyAcceptBinaryValue = true;
        private static int[] BinaryAcceptValues = {2};
        

        static void Main(string[] args)
        {
            string path;

            if (args.Length > 0)
            {
                path = args[0];
            }
            else
            {
                Console.WriteLine("Please enter path to .csv file!");
                path = Console.ReadLine();
            }

            if (!File.Exists(path))
            {
                Console.WriteLine("File does not exist!");
            }
            else
            {
                string directory = Path.GetDirectoryName(path);

                List<Machine> machines = AnalysingService.AnalyseCSV(path);
                bool result = CSVConverterService.ConvertCSV(machines, directory, Interval, OnlyAcceptBinaryValue, BinaryAcceptValues, UseShortNotationForm);

                if (result)
                {
                    Console.WriteLine($"Successfully converted to {machines.Sum(x => x.WorkDays.Count)} CSV files.");
                }
                else
                {
                    Console.WriteLine("Converting failed!");
                }
            }

            Console.ReadLine();
        }
    }
}
