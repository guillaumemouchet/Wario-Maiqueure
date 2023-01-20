using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ItemCollector : MonoBehaviour
{
    private int strawberries = 0;
    [SerializeField] private Text strawberriesText;
    [SerializeField] private AudioSource collectSound;

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if(collision.gameObject.CompareTag("Strawberry"))
        {
            collectSound.Play();
            strawberries++;
            Destroy(collision.gameObject);
            strawberriesText.text = "Strawberries: " + strawberries;
        }
    }
}
