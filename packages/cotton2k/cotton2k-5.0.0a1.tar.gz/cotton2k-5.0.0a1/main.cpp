//
// Created by Tang on 11/13/2020.
//
#include "cotton2k.h"

using namespace std;
namespace fs = std::filesystem;

namespace cotton2k{
    void run(const string& profile)
    {
        fs::path base = "profiles";
        fs::path profile_file_path = base / profile;
        ifstream file(profile_file_path, ios::in);
        if (file.fail())    
            cout << profile_file_path << endl;
        ProfileName = profile_file_path.stem().string();
        file.close();
        ReadInput();
        cout << "Running the Simulation" << endl;
        daily_simulation();
        cout << "Writing Output Files" << endl;
        DataOutput();
    }
    void daily_simulation()
    {
        Daynum = DayStart - 1;
        bEnd = false;

        while (!bEnd)
        {
            bool bAdjustToDo = adjust();
            simulate();
            if (bAdjustToDo)
                WriteStateVariables(true);
        }
    }
    bool adjust()
    {
        static int kprevadj = 0;
        int sumsad = accumulate(MapDataDate, MapDataDate + 30, 0);
        if (sumsad <= 0)
            return false;
        for (int i = 0; i < 30; i++)
        {
            if (Daynum == MapDataDate[i])
            {
                NumAdjustDays = Kday - kprevadj;
                if (NumAdjustDays > 12)
                    NumAdjustDays = 12;
                for (int jj = 0; jj < 5; jj++)
                {
                    PlantAdjustments(i, jj);
                    if (nadj[jj])
                        for (int j1 = 0; j1 < NumAdjustDays; j1++)
                        {
                            simulate();
                            if (Kday > 0)
                                WriteStateVariables(true);
                        }
                }

                kprevadj = MapDataDate[i] - DayEmerge + 1;
                MapDataDate[i] = 0;
                for (int jj = 0; jj < 5; jj++)
                    nadj[jj] = false;
                continue;
            }
        }
        return true;
    }
    void simulate()
    {
        Daynum++;
        Date = DoyToDate(Daynum, iyear);
        DayOfSimulation = Daynum - DayStart + 1;
        if (DayEmerge <= 0)
            Kday = 0;
        else
            Kday = Daynum - DayEmerge + 1;
        if (Kday < 0)
            Kday = 0;
        
        ColumnShading();
        DayClim();
        SoilTemperature();
        SoilProcedures();
        SoilNitrogen();
        SoilSum();

        if (Daynum >= DayEmerge && isw > 0)
        {
            isw = 2;
            DayInc = PhysiologicalAge();
            if (pixday[0] > 0)
                Pix();
            Defoliate();
            Stress();
            GetNetPhotosynthesis();
            PlantGrowth();
            CottonPhenology();
            PlantNitrogen();
            CheckDryMatterBal();

            if (OutIndex[20] > 0)
            {
                PlantNitrogenBal();
                SoilNitrogen();
                SoilNitrogenAverage();
            }
        }
        DailyOutput();

        if (Daynum >= DayFinish || Daynum >= LastDayWeatherData || (Kday > 10 && LeafAreaIndex < 0.0002))
            bEnd = true;
    }
    vector<string> get_profiles(const string& job_file)
    {
        ifstream file(job_file, ios::in);
        if (file.fail())
            throw 1;
        vector<string> result;
        string line;
        getline(file, line); // Skip first line
        while (getline(file, line))
            result.push_back(line);
        file.close();
        return result;
    }
}

int main(int argc, char *argv[])
{
    if (argc != 2)
        return 1;
    string job_file = argv[1];
    vector<string> profiles = cotton2k::get_profiles(job_file);
    for (const string& profile : profiles)
    {
        cotton2k::run(profile);
    }
    return 0;
}
