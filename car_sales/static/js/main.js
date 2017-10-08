$(document).ready(
    $(function() {
        // jQuery selection for the 2 select boxes
        var dropdown = {
            make: $('#make'),
            model: $('#model')
        };

        // call to update on load
        updateModels(true);

        // function to call XHR and update model dropdown
        function updateModels(onPageLoad) {
            var send = {
                make: dropdown.make.val()
            };
            dropdown.model.attr('disabled', 'disabled');
            dropdown.model.empty();
            if(onPageLoad === false){
                debugger;
                $.ajax({
                     url:'/stock/return_models/'+send.make,
                     success: function(data) {
                        data.forEach(function(item) {
                            dropdown.model.append(
                            $('<option>', {
                                value: item[0],
                                text: item[1]
                            })
                        );
                        dropdown.model.removeAttr('disabled');
                     })},
                     failure: function(response){
                        console.log("Failure");
                     }
                });
            }
        };

        // event listener to make dropdown change
        dropdown.make.on('change', function() {
            updateModels(false);
        });
    })
);
