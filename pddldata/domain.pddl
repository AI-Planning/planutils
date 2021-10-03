(define (domain blocksworld)

  (:requirements :strips)

  (:predicates (on ?x ?y)

                   (ontable ?x)

                   (clear ?x)

                   (arm-free)

                   (holding ?x)

                   )

 

  (:action pick-up

                 :parameters (?x)

                 :precondition (and (clear ?x) (ontable ?x) (arm-free))

                 :effect

                 (and (not (ontable ?x))

                           (not (clear ?x))

                           (not (arm-free))

                           (holding ?x)))

 

  (:action put-down

                 :parameters (?x)

                 :precondition (holding ?x)

                 :effect

                 (and (not (holding ?x))

                           (clear ?x)

                           (arm-free)

                           (ontable ?x)))

  (:action stack

                 :parameters (?x ?y)

                 :precondition (and (holding ?x) (clear ?y))

                 :effect

                 (and (not (holding ?x))

                           (not (clear ?y))

                           (clear ?x)

                           (arm-free)

                           (on ?x ?y)))

  (:action unstack

                 :parameters (?x ?y)

                 :precondition (and (on ?x ?y) (clear ?x) (arm-free))

                 :effect

                 (and (holding ?x)

                           (clear ?y)

                           (not (clear ?x))

                           (not (arm-free))

                           (not (on ?x ?y)))))