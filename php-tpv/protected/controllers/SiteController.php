<?php
# @Author: Manuel Rodriguez <valle>
# @Date:   23-May-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 23-May-2018
# @License: Apache license vesion 2.0


  /**
   * Clase creada solo para testear el servicio web
   *  aun no hace nada pero se le agregara algunos servicios.
   * @author vallesoft.es
   */
    class SiteController extends CController{

        public function actionIndex(){
           header("Location: /gestion");
        }

    }
?>
