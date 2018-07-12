<?php
# @Author: Manuel Rodriguez <valle>
# @Date:   23-May-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 27-Jun-2018
# @License: Apache license vesion 2.0

/**
 * Registro base para todos las lineas de una tabla.
 * @author vallesoft.es
 */
class Registro extends CActiveRecord {

     public static function model($className = __CLASS__) {
         $className = get_called_class();
         return parent::model($className);
     }


     /// Devuelve un array de registros con una condicion si no por defecto develve todos.
     /// y con un limite de registros.
     public function queryLimit($numMax,$numIni, $condition='',$params=array()) {
        $criteria=$this->getCommandBuilder()->createCriteria($condition, $params);
        $this->applyScopes($criteria);
        $command=$this->getCommandBuilder()->createFindCommand($this->getTableSchema(),$criteria);
        $command->limit($numMax,$numIni);
        $results = $command->queryAll();
        return $results;
    }

     /// Devuelve un array de registros con una condicion si no por defecto develve todos.
     public function queryAll($condition='',$params=array()) {
        $criteria=$this->getCommandBuilder()->createCriteria($condition, $params);
        $this->applyScopes($criteria);
        $command=$this->getCommandBuilder()->createFindCommand($this->getTableSchema(),$criteria);
        $results = $command->queryAll();
        return $results;
    }

     /// Devuelve un array de registros con una condicion si no por defecto develve todos.
     public function queryAllCDb(CDbCriteria $criteria) {
        $this->applyScopes($criteria);
        $command=$this->getCommandBuilder()->createFindCommand($this->getTableSchema(),$criteria);
        $results = $command->queryAll();
        return $results;
    }
}
