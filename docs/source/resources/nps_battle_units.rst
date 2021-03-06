#################################################################
National Park Service combined battle data: Battle in each battle
#################################################################

:name: nps_battle_units
:path: nps_battle_units.csv
:format: csv

Union and Confederate units in each battle.

This is a slightly edited version of the CWSS battle units data. See :doc:`cwss_battle_units`.


Sources: 


Schema
======



===========  ======  ===========
cwsac_id     string  CWSAC Id.
belligerent  string  belligerent
unit_code    string  unit_code
companies    number  companies
batteries    number  batteries
detachment   number  detachment
section      number  section
added        string  added
src          string  Source
comment      string  comment
===========  ======  ===========

cwsac_id
--------

:title: CWSAC Id.
:type: string
:format: default
:constraints:
    :minLength: 5
    :maxLength: 6
    :pattern: [A-Z]{2}[0-9]{3}[A-Z]?
    

CWSAC battle identifier


       
belligerent
-----------

:title: belligerent
:type: string
:format: default
:constraints:
    :enum: ['US', 'Confederate']
    

Side of the force: Confederate or Union or Native American.


       
unit_code
---------

:title: unit_code
:type: string
:format: default





       
companies
---------

:title: companies
:type: number
:format: default





       
batteries
---------

:title: batteries
:type: number
:format: default





       
detachment
----------

:title: detachment
:type: number
:format: default





       
section
-------

:title: section
:type: number
:format: default





       
added
-----

:title: added
:type: string
:format: default


If ``true``, then this was in the original CWSS data. If ``false``, then this unit was added by the author for this dataset.
Currently, the only units added were those appearing in battles omitted from the original CWSS data.


       
src
---

:title: Source
:type: string
:format: default


Original source for the CWSS data.


       
comment
-------

:title: comment
:type: string
:format: default





       

