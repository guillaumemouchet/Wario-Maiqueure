using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Rotate : MonoBehaviour
{
    [SerializeField] private float speed = 1.7f;
    // Update is called once per frame
    private void Update()
    {
        transform.Rotate(0,0,-Time.deltaTime*speed*360);
    }
}
