# Todo List

- Quand l'alarme sonne, elle doit sonner tant que l'user ne l'a pas désactivée.
- La désactivation de l'alarme se fait par différents moyens, comme le bouton sur la tête du nabaztag, l'app ou la
  détection de mouvement.
- voir pattern strategy pour la désactivation de l'alarme

- raccorder le haut parleur à la Raspberry
- raccorder le bouton à la Raspberry
- raccorder le capteur de mouvement à la Raspberry
- raccorder l'arduino à la Raspberry et mettre en place la communication série
- faire le programme pour envoyer du son vers le haut parleur

## Bugs

## Features

    - 30 min avant un évènement, le rappeller à l'utilisateur

## Ideas

    - Si l'utilisateur n'a pas de réveil, on lui propose de le mettre
    - La météo doit s'actualiser quand on la demande

## Improvements
    - l'heure doit se mettre à jour par rapport à l'heure d'internet, et il faut l'utiliser partout du coup
    - se débarasser du .replace(tzinfo=timezone(offset=timedelta(hours=2))) dans le code

## Documentation

    - documenter les fonctions manquantes

## Tests
    - Trouver le premier event de la journée, et si c'est le matin, on met une alarme pour le réveil

## Refactoring

## Other

## Done

    - récuperer les prochains évènements de l'agenda toutes les heures
    - La météo ne doit pas s'actualiser en permanence
    - il faudrait qu'une heure avant l'alarme, on fasse un call pour obtenir la météo


    - L'alarme sonne, mais une alarme est set à nouveau pour le même event. Puis l'alarme re-sonne dans la même minute à l'actualisation d'après
        Donc, quand l'alarme de l'évènement sonne, on doit différencier le current event et le next event

