#!/bin/bash

ecm=365
scen=3


let ecmm15=$ecm-15
let ecmp1=$ecm+1

echo "Processing $ecm with 5 GeV steps until $ecmm15"

rm input_newprod_fcc_scenario${scen}_ecm${ecm}.dat;
rm input_newprod_fcc_scenario${scen}_ecm${ecm}_withLam345.dat;

mhmin=70;

#240 GeV
#for i in `seq 0 10`; do
#365 GeV
for i in `seq 0 22`; do

    let mh=$mhmin+5*$i;
    if [ "$scen" -eq 1 ]; then
	lam345=0
    else
	lam345=$(echo "0.0018 * ($mh - 72)" | bc)
    fi
    
    for k in `seq 0 4`; do
	let ma=$mhmin+5*$i+2*$k+2;
	let mhch=$ma;
	let mdiff=$ma-$mh;
	if [ "$scen" -eq 3 ]; then
	    if [ "$mdiff" -lt 21 ]; then
		let mhch=$ma+60;
	    elif [ "$mdiff" -lt 51 ]; then
		let mhch=$ma+50;
	    elif [ "$mdiff" -lt 81 ]; then
		let mhch=$ma+40;
	    elif [ "$mdiff" -lt 121 ]; then
		let mhch=$ma+30;
	    elif [ "$mdiff" -lt 136 ]; then
		let mhch=$ma+20;
	    else
		let mhch=$ma+5;
	    fi
	fi
	
	let msum=$ma+$mh;

	if [ "$msum" -lt "$ecmp1" ]; then
	    echo $mh", "$ma", "$mhch", "$msum", "$mdiff", "$lam345
	    echo $mh", "$ma", "$mhch >> input_newprod_fcc_scenario${scen}_ecm${ecm}.dat;
	    echo $mh", "$ma", "$mhch", "$lam345 >> input_newprod_fcc_scenario${scen}_ecm${ecm}_withLam345.dat;
	fi;
	
    done;
#    for j in `seq 2 19`;
    for j in `seq 2 44`;
    do

	let ma=$mhmin+5*$i+5*$j+5;
	let mhch=$ma;
	let msum=$ma+$mh;
	let mdiff=$ma-$mh;
	if [ "$scen" -eq 3 ]; then
	    if [ "$mdiff" -lt 21 ]; then
		let mhch=$ma+60;
	    elif [ "$mdiff" -lt 51 ]; then
		let mhch=$ma+50;
	    elif [ "$mdiff" -lt 81 ]; then
		let mhch=$ma+40;
	    elif [ "$mdiff" -lt 121 ]; then
		let mhch=$ma+30;
	    elif [ "$mdiff" -lt 136 ]; then
		let mhch=$ma+20;
	    else
		let mhch=$ma+5;
	    fi
	fi

	if [ "$msum" -lt "$ecmm15" ]; then
	    echo $mh", "$ma", "$mhch", "$msum", "$mdiff", "$lam345
	    echo $mh", "$ma", "$mhch >> input_newprod_fcc_scenario${scen}_ecm${ecm}.dat;
	    echo $mh", "$ma", "$mhch", "$lam345 >> input_newprod_fcc_scenario${scen}_ecm${ecm}_withLam345.dat;
	    
	else
	    break;
	fi;
    done;
    for k in `seq 0 9`; do
	let ma=$mhmin+5*$i+5*$j+2*$k+2;
	let msum=$ma+$mh;
	let mdiff=$ma-$mh;
	let mhch=$ma;
	if [ "$scen" -eq 3 ]; then
	    if [ "$mdiff" -lt 21 ]; then
		let mhch=$ma+60;
	    elif [ "$mdiff" -lt 51 ]; then
		let mhch=$ma+50;
	    elif [ "$mdiff" -lt 81 ]; then
		let mhch=$ma+40;
	    elif [ "$mdiff" -lt 121 ]; then
		let mhch=$ma+30;
	    elif [ "$mdiff" -lt 136 ]; then
		let mhch=$ma+20;
	    else
		let mhch=$ma+5;
	    fi
	fi

	if [ "$msum" -lt "$ecmp1" ]; then
	    echo $mh", "$ma", "$mhch", "$msum", "$mdiff" "$lam345
	    echo $mh", "$ma", "$mhch >> input_newprod_fcc_scenario${scen}_ecm${ecm}.dat;
	    echo $mh", "$ma", "$mhch", "$lam345 >> input_newprod_fcc_scenario${scen}_ecm${ecm}_withLam345.dat;
	fi;
	
    done;
    

done

#240 GeV
#for i in `seq 0 10`; do
#365 GeV
#for i in `seq 0 22`; do
#    let mh=$mhmin+5*$i;
#    if [ "$scen" -eq 1 ]; then
#	lam345=0
#    else
#	lam345=$(echo "0.0018 * ($mh - 72)" | bc)
#    fi
#   
#   echo $mh", "$lam345
#done
