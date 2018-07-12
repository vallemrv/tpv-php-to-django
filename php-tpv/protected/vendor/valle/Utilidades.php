<?php
# @Author: Manuel Rodriguez <valle>
# @Date:   23-May-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 27-Jun-2018
# @License: Apache license vesion 2.0

/**
 * Description of Utilidades
 *
 * @author elvalle
 */
class Utilidades {
    //put your code here
    public static function RotarFecha($fechastr){
   	   $arFecha = explode("/", $fechastr);
	     $mes = strlen($arFecha["1"])==1?"0".$arFecha["1"]:$arFecha["1"];
	     $dia = "";
	     $year = "";
	     if(strlen($arFecha["0"])<4){
  	     $dia = strlen($arFecha["0"])==1?"0".$arFecha["0"]:$arFecha["0"];
  	     $year = $arFecha["2"];
  	     return $year."/".$mes."/".$dia;
	     }else{
  	     $dia = strlen($arFecha["2"])==1?"0".$arFecha["2"]:$arFecha["2"];
  	     $year = $arFecha["0"];
  	     return $dia."/".$mes."/".$year;
	     }
   }
}
