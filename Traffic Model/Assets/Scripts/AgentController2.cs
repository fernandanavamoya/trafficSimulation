// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz.
// Octavio Navarro. October 2021

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

public class TrafficLightData
{
    public bool state;
    public Vector3 position;
}

public class CarsData
{
    public List<Vector4> positions;
}

public class AgentController2 : MonoBehaviour
{
    // private string url = "https://boids.us-south.cf.appdomain.cloud/";
    string serverUrl = "http://localhost:8585";
    string getCarsEndpoint = "/getCars";
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";
    CarsData carsData, obstacleData;
    Dictionary<int, Vector3> oldPositions;
    Dictionary<int, Vector3> newPositions;
    bool hold = false;
    public Dictionary<int, GameObject> agents;

    public GameObject carPrefab;
    public int NAgents, maxIterations;
    public float timeToUpdate = 5.0f, timer, dt;

    void Start()
    {
        carsData = new CarsData();
        oldPositions = new Dictionary<int, Vector3>();
        newPositions = new Dictionary<int, Vector3>();

        agents = new Dictionary<int, GameObject>();
        
        timer = timeToUpdate;

        for(int i = 0; i < NAgents; i++) {
            agents[i] = Instantiate(carPrefab, Vector3.zero, Quaternion.identity);
        }
        StartCoroutine(SendConfiguration());
    }

    private void Update() 
    {
        float t = timer/timeToUpdate;
        // Smooth out the transition at start and end
        dt = t * t * ( 3f - 2f*t);

        if(timer >= timeToUpdate)
        {
            timer = 0;
            hold = true;
            StartCoroutine(UpdateSimulation());
        }
        if (!hold)
        {
            foreach (KeyValuePair<int, Vector3> s in newPositions)
            {
                int id = s.Key;
                Vector3 interpolated = Vector3.Lerp(oldPositions[id], newPositions[id], dt);
                agents[id].transform.localPosition = interpolated;
                
                Vector3 dir = oldPositions[id] - newPositions[id];
                if (oldPositions[id] != newPositions[id]) {
                    agents[id].transform.rotation = Quaternion.LookRotation(dir);
                }
            }
            // Move time from the last frame
            timer += Time.deltaTime;
        }
    }
 
    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            StartCoroutine(GetCarsData());
        }
    }

    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();

        form.AddField("NAgents", NAgents.ToString());
        form.AddField("maxIterations", maxIterations.ToString());

        UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            Debug.Log("Configuration upload complete!");
            Debug.Log("Getting Agents positions");
            StartCoroutine(GetCarsData());
        }
    }

    IEnumerator GetCarsData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getCarsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            Debug.Log(www.downloadHandler.text);
            carsData = JsonUtility.FromJson<CarsData>(www.downloadHandler.text);

            // Store the old positions for each agent
            oldPositions = new Dictionary<int, Vector3>(newPositions);

            newPositions.Clear();

            foreach(Vector4 pos in carsData.positions) {
                newPositions[(int)pos.w] = pos;
            }

            hold = false;
        }
    }

    // IEnumerator GetObstacleData() 
    // {
    //     UnityWebRequest www = UnityWebRequest.Get(serverUrl + getObstaclesEndpoint);
    //     yield return www.SendWebRequest();
 
    //     if (www.result != UnityWebRequest.Result.Success)
    //         Debug.Log(www.error);
    //     else 
    //     {
    //         obstacleData = JsonUtility.FromJson<CarsData>(www.downloadHandler.text);

    //         Debug.Log(obstacleData.positions);

    //         foreach(Dictionary<string, int> position in obstacleData.positions)
    //         {
    //             Instantiate(obstaclePrefab, position, Quaternion.identity);
    //         }
    //     }
    // }
}
