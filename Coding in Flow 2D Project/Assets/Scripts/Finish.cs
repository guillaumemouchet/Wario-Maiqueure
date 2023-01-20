using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
public class Finish : MonoBehaviour
{
    private AudioSource finishSound;
    private bool finished = false;
    // Start is called before the first frame update
    private void Start()
    {
        finishSound = GetComponent<AudioSource>();
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        Debug.Log("OUT");
        if(collision.gameObject.name == "Player" && !finished)
        {
            Debug.Log("INN");
            finishSound.Play();
            finished = true;
            Invoke("CompleteLevelCompilateur", 2f);
        }
        
    }

    private void CompleteLevel()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex + 1);
    }

    private void CompleteLevelCompilateur()
    {
        SceneManager.LoadScene("End Scene");
    }
}
