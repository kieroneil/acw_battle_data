####################################################################
Strengths and casualties for forces in the civilwar.org battle data.
####################################################################

:name: civilwarorg_forces
:path: civilwarorg_forces.csv
:format: csv

Casualties and strengths of forces in battles from the `Civil War Trust <http://www.civilwar.org/>`__.
See :doc:`civilwarorg_battles`.


Sources: 


Schema
======



================  =======  ====================
battle_id         string   Battle
belligerent       string   Belligerent
strength          integer  Strength
casualties        integer  Total casualties
killed            integer  Killed
wounded           integer  Wounded
killed_wounded    number   killed_wounded
missing_captured  integer  Missing and Captured
================  =======  ====================

battle_id
---------

:title: Battle
:type: string
:format: default





       
belligerent
-----------

:title: Belligerent
:type: string
:format: default
:constraints:
    :enum: ['US', 'Confderate']
    




       
strength
--------

:title: Strength
:type: integer
:format: default
:constraints:
    

Troops engaged in the battle.


       
casualties
----------

:title: Total casualties
:type: integer
:format: default
:constraints:
    




       
killed
------

:title: Killed
:type: integer
:format: default
:constraints:
    




       
wounded
-------

:title: Wounded
:type: integer
:format: default
:constraints:
    




       
killed_wounded
--------------

:title: killed_wounded
:type: number
:format: default





       
missing_captured
----------------

:title: Missing and Captured
:type: integer
:format: default
:constraints:
    




       

