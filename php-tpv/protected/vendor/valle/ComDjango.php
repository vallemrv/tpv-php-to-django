<?php
# @Author: Manuel Rodriguez <valle>
# @Date:   27-Jun-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 04-Jul-2018
# @License: Apache license vesion 2.0

/**
 * Description of ComDjango
 * clase para la portacion del proyeto php a django.
 * @author valle
 */
class ComDjango {
    //put your code here
    static function ImprimirPedido($url, $id){
          $ch = curl_init($url."ventas/imprimir_pedido/".$id."/");
          curl_setopt($ch, CURLOPT_HEADER, 0);
          curl_exec($ch);
          curl_close($ch);
    }

    static function PreImprimirPedido($url, $id){
          $ch = curl_init($url."ventas/preimprimir_pedido/".$id."/");
          curl_setopt($ch, CURLOPT_HEADER, 0);
          curl_exec($ch);
          curl_close($ch);
    }

    static function PreImprimirTicket($url, $id){
          $ch = curl_init($url."ventas/preimprimir_ticket/".$id."/");
          curl_setopt($ch, CURLOPT_HEADER, 0);
          curl_exec($ch);
          curl_close($ch);
    }

    static function ImprimirTicket($url, $id){
          $ch = curl_init($url."ventas/imprimir_ticket/"
                          .$id."/");
          curl_setopt($ch, CURLOPT_HEADER, 0);
          curl_exec($ch);
          curl_close($ch);
    }

    static function ReeviarLinea($url, $idp, $id, $nombre){
          $ch = curl_init($url."ventas/reenviarlinea/".$idp."/".$id."/".urlencode($nombre)."/");
          curl_setopt($ch, CURLOPT_HEADER, 0);
          curl_exec($ch);
          curl_close($ch);
    }

    static function AbrirCajon($url){
          $ch = curl_init($url."ventas/abrircajon/");
          curl_setopt($ch, CURLOPT_HEADER, 0);
          curl_exec($ch);
          curl_close($ch);
    }

    static function ImprimirArqueo($url, $id){
        $ch = curl_init($url."ventas/imprimir_desglose/".$id."/");
        curl_setopt($ch, CURLOPT_HEADER, 0);
        curl_exec($ch);
        curl_close($ch);
    }



}
