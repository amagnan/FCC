!
! File: Pythia_LHEinput.cmd 
!
! This file contains commands to be read in for a Pythia8 run.
! Lines not beginning with a letter or digit are comments.
! Names are case-insensitive  -  but spellings-sensitive!
! Adjusted from Pythia example: main42.cmnd

! 1) Settings that will be used in a main program.
Random:setSeed = on
Main:numberOfEvents = <NEVTS>          ! number of events to generate
Main:timesAllowErrors = 100        ! abort run after this many flawed events

! 2) Settings related to output in init(), next() and stat() functions.
Init:showChangedSettings = on      ! list changed settings
Init:showAllSettings = off         ! list all settings
Init:showChangedParticleData = on  ! list changed particle data
Init:showAllParticleData = off     ! list all particle data
Next:numberCount = 1000            ! print message every n events
Next:numberShowLHA = 2             ! print LHA information n times
Next:numberShowInfo = 2            ! print event information n times
Next:numberShowProcess = 2         ! print process record n times
Next:numberShowEvent = 2           ! print event record n times
Stat:showPartonLevel = off         ! additional statistics on MPI
Stat:showProcessLevel = off         ! additional statistics on MPI

! 4) Read-in Les Houches Event file - alternative beam and process selection.
Beams:frameType = 4                      ! read info from a LHEF
Beams:SetProductionScalesFromLHEF = off
Beams:LHEF = <LHEFILE> ! the LHEF to read from

! Vertex smearing :
Beams:allowVertexSpread = on
Beams:sigmaVertexX = 9.70e-3   !  13.7 mum / sqrt2
Beams:sigmaVertexY = 25.5E-6   !  36.1 nm / sqrt2
Beams:sigmaVertexZ = 0.64      !  0.64 mm
 
ProcessLevel:all = off             ! To allow hadronisation only
PartonLevel:ISR = on               ! initial-state radiation
PartonLevel:FSR = on               ! final-state radiation

! Tau decays to mu nu_tau nu_mu (from pythia8)
!15:onMode = off
!15:onIfAny = 14
