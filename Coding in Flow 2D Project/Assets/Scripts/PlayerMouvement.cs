using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMouvement : MonoBehaviour
{
    private Rigidbody2D rb;
    private Animator anim;
    private SpriteRenderer sprite;
    private BoxCollider2D col;
    [SerializeField] private LayerMask jumpableGround;
    private enum MovementState
    {
        idle,
        running,
        jumping,
        falling
    };

    [SerializeField] private AudioSource jumpSound;

    private float dirX = 0;

    [SerializeField]private float moveSpeed = 7;
    [SerializeField]private float jumpforce = 14;
    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        anim = GetComponent<Animator>();
        sprite = GetComponent<SpriteRenderer>();
        col = GetComponent<BoxCollider2D>();
            }

    // Update is called once per frame
    void Update()
    {
        dirX = Input.GetAxisRaw("Horizontal");
        rb.velocity = new Vector2(dirX * moveSpeed, rb.velocity.y);

        UpdateAnimationState();

        if (Input.GetButtonDown("Jump") && IsGrounded())
        {
            jumpSound.Play();
            rb.velocity = new Vector2(rb.velocity.x, jumpforce);
        }

        
    }

    private void UpdateAnimationState()
    {
        MovementState animState;
        if(dirX>0)
        {
            animState = MovementState.running;
            sprite.flipX = false;

        }
        else if(dirX<0)
        {
            animState = MovementState.running;
            sprite.flipX = true;
        }
        else
        {
            animState = MovementState.idle;
        }

        if(rb.velocity.y>.001f)
        {
            animState= MovementState.jumping;
        }else if(rb.velocity.y < -.001f)
        {
            animState = MovementState.falling;
        }

        anim.SetInteger("state", (int)animState);
    }
    private bool IsGrounded()
    {
        return Physics2D.BoxCast(col.bounds.center, col.bounds.size, 0, Vector2.down, .1f, jumpableGround );
    }
}
