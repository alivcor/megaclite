define([
        'require',
        'base/js/namespace',
        'jquery',
        'base/js/utils',
        'base/js/dialog'
], function(requirejs, Jupyter, $, utils, dialog) {

    function show_usage(){
        var script_path = requirejs.toUrl("./megaclite.png");
        var jh_username = utils.get_body_data('baseUrl').match(/.*\/user\/(.*)\//)[1]
        var megacliteUrl = utils.url_path_join(utils.get_body_data('baseUrl'), 'megaclite/' + jh_username)
        $.getJSON(megacliteUrl, function(data){
                $("#maintoolbar-container").append("<img src=\"" + script_path + "\"  style=\"display: inline; max-width: 100px; padding-left:20px;\"/><span id=\"megaclite\"> &nbsp; <b> Memory Utilization : <span id=\"actual_val\">" + data['actual_val'] + "</span> MB </b></span>");

            });
    }

    var warn_alerted = false;
    var error_alerted = false;


    function update_usage() {
        var jh_username = utils.get_body_data('baseUrl').match(/.*\/user\/(.*)\//)[1]
        var megacliteUrl = utils.url_path_join(utils.get_body_data('baseUrl'), 'megaclite/' + jh_username)
        $.getJSON(megacliteUrl, function(data) {
            if(data['actual_val'] == null){
                document.getElementById("actual_val").innerHTML = "Kernel appears to be dead.";
            } else {
                document.getElementById("actual_val").innerHTML = data['actual_val'];

                if(data['zone'] == "S"){
                    document.getElementById("megaclite").style = "color: #339900;";
                } else {
                    if(data['zone'] == "W"){
                        document.getElementById("megaclite").style = "color: #8B4513;";
                        if(warn_alerted != true){
                            dialog.modal(data);
                            warn_alerted = true;

                        }
                    } else {
                        document.getElementById("megaclite").style = "color: #d9534f;";
                        if(error_alerted != true){
                            dialog.modal(data);
                            error_alerted = true;
                        }

                    }


                }


            }



        });

    }




    function load_info_label(){
        show_usage();
        update_usage();
        if(!Jupyter.toolbar) {
            $([Jupyter.events]).on("app_initialized.NotebookApp", load_info_label);
            return;
        }
        setInterval(update_usage, 10*1000);
    }


    function load_ipython_extension() {
        load_info_label();
    }


    return {
        load_ipython_extension: load_ipython_extension
    };


})
