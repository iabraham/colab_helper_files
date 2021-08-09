# grav is a correction for the weight of the transducer
grav = 18.7969

# These labels are all the files with the maximum voluntary
# contractions
LabelMVC = ['MVC01R', 'MVC02R', 'MVC03R', 'MVC04R', 'MVC05R',
            'MVC06B', 'MVC07R', 'MVC08R', 'MVC09R', 'MVC10R',
            'MVC11R', 'MVC12R', 'MVC13R', 'MVC14B', 'MVC15B',
            'MVC16B', 'MVC01L', 'MVC02L', 'MVC03L', 'MVC04L',
            'MVC05L', 'MVC06B', 'MVC07L', 'MVC08L', 'MVC09L',
            'MVC10L', 'MVC11L', 'MVC12L', 'MVC13L', 'MVC14B',
            'MVC15B', 'MVC16B']

# Set up the array for the tests performed to traverse the analog
# # and forceq# data
Tests = ['Right_upper_arm_max_push', 'Right_upper_arm_max_pull',
         'Right_upper_arm_30_push ', 'Right_upper_arm_30_pull ',
         'Right_forearm_max_push  ', 'Right_forearm_max_pull  ',
         'Right_forearm_30_push   ', 'Right_forearm_30_pull   ',
         'Right_thigh_max_push    ', 'Right_thigh_max_pull    ',
         'Right_thigh_30_push     ', 'Right_thigh_30_pull     ',
         'Right_shin_max_push     ', 'Right_shin_max_pull     ',
         'Right_shin_30_push      ', 'Right_shin_30_pull      ']


muscles = ['Middle Deltoid                   ', #1, 17
           'Triceps Brachialis (Lateral Head)', #2, 18
           'Biceps Brachii                   ', #3, 19
           'Extensor Carpi Radialis          ', #4, 20
           'Flexor Carpi Radialis            ', #5, 21
           'Upper Trapezius                  ', #6, 22
           'Infraspinatus                    ', #7, 23
           'Latissimus Dorsi                 ', #8, 24
           'Semitendinosus                   ', #9, 25
           'Adductor Magnus                  ', #10, 26
           'Rectus Femoris                   ', #11, 27
           'Vastus Medialis                  ', #12, 28
           'Anterior Tibialis                ', #13, 29
           'Medial Gastrocnemius             ', #14, 30
           'Rectus Abdominus                 ', #15, 31
           'Erector Spinae                   '] #16, 32

calibrate = [[0.02375, 0.18892, -2.30844, -69.85071, 1.12790,
              68.4637], 
            [2.37034, 79.92851, -1.47167, -40.50485, -0.13308,
             -39.33057], 
            [119.81241, -2.44853, 122.64353, 0.25764, 118.71703,
             0.57416], 
            [-0.00790, 0.96511, -4.20187, -0.48994, 4.12478,
             -0.46217], 
            [4.77499, -0.10348, -2.40995, 0.84289, -2.38393,
             -0.83158],
            [-0.10331, -2.63117, -0.06771, -2.66325, -0.02935,
             -2.62106]]
