<?php
# @Author: Manuel Rodriguez <valle>
# @Date:   23-May-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 27-Jun-2018
# @License: Apache license vesion 2.0
/**
 * Description of RefrescoController
 *
 * @author valle
 */
class SyncController extends CController {
    //put your code here
    public function actionGetUpdate(){
       $res = array();
       try {
         $hora = isset($_POST["hora"]) ? $_POST["hora"] : "";
         if($hora=="") $res = array("hora"=>date("Y/m/d - H:i:s"),
                                    "Tablas"=>array(
                                             array("Tabla"=>"Camareros"),
                                             array("Tabla"=>"Zonas"),
                                             array("Tabla"=>"Secciones"),
                                             array("Tabla"=>"MesasAbiertas"),
                                             array("Tabla"=>"SubTeclas"),
                                             array("Tabla"=>"TeclasCom")
                                           ));
         else{
           $sync = new Sync();
           $condicion = new CDbCriteria();
           $condicion->addCondition("Modificado>='$hora'");
           $condicion->group = "Tabla";
           $condicion->order = "Modificado DESC";
           $res = array("hora"=>date("Y/m/d - H:i:s"),"Tablas"=>$sync->queryAllCDb($condicion));
         }
       } catch (Exception $e) {
          error_log($e->getMessage());
       } finally {
          echo json_encode($res);
       }
    }
}
