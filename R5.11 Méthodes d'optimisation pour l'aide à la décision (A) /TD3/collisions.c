struct Sprite
{
    int g, b, h, d;
    
    char *chemain_icone;

    unsigned int len_chemain_icone;
};

int collision_non_vide(struct Sprite sprite1, struct Sprite sprite2)
{
    int ok_h = (sprite1.g < sprite2.d) && (sprite1.d > sprite2.g);
    int ok_v = (sprite1.b < sprite2.h) && (sprite1.h > sprite2.b);
    return ok_h && ok_v;
}

int compte_collisions(struct Sprite *sprites, unsigned int nb_sprites)
{
    int nb_collisions = 0;
    for (unsigned int i = 0; i < nb_sprites; i++)
    {
        for (unsigned int j = i + 1; j < nb_sprites; j++)
        {
            if (collision_non_vide(sprites[i], sprites[j]))
            {
                nb_collisions++;
            }
        }
    }
    return nb_collisions;
}