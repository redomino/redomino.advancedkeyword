/*
jquery keywordtree

manage keyword tree keeping a select and a tree of checkboxes synced
*/

jQuery.fn.keywordtree = function (select){
    return this.each(function (){
        
        var $tree = jQuery(this);
        var $select = jQuery(select);
        // step 1 update the original widget 
        $tree.delegate('input', 'click', function (){
            var $this = $(this);
            // step 3
            if($this.is(':checked')){
                //select all the ancestor
                $this.parents('li').children('input').attr('checked', 'checked');
            }
            else {
                //unselect all the descendents
                $this.closest('li').find('input').removeAttr('checked');
            }
            // step 4
            $select.empty();
            $tree.find('input').each(function (){
                var $this = jQuery(this);
                var $opt = jQuery('<option value="' + $this.val() +'">' + $this.val() + '</option>');
                if ($this.is(':checked')){
                    $opt.attr('selected', 'selected').addClass('selected');
                }
                $opt.appendTo($select);
            });
        });
    });
};


jQuery.fn.collapsedtree = function (){
    var filter_label = window.REDOMINO_ADVANCED_KEYWORD && window.REDOMINO_ADVANCED_KEYWORD.filter_label || 'filter:';
    return this.each(function (){

        var $tree = jQuery(this);
        var open = function ($placeholder,speed){
            $placeholder
                .addClass('opened')
                .siblings('ul')
                .show(speed);
                
            var $ul = $placeholder.closest('ul');
            if (! $ul.is('.collapsedtree')){
                open($ul.closest('li').children('.placeholder'));
            }

        };
        var close = function ($placeholder, speed){
            $placeholder
                .removeClass('opened')
                .siblings('ul')
                .hide(speed);
        };

        var changeTimer;
        // searchbox
        jQuery('<input placeholder="..."/>').keyup(function (){
            clearTimeout(changeTimer);
            var $this = jQuery(this);
            changeTimer = setTimeout(function (){
                var s = $this.val().toLocaleLowerCase();
                $tree.find('label').removeClass('found');
                $tree.find('.placeholder').each(function (){
                    close($(this));
                });

                if (s){
                    
                    $tree.find('label')
                    .filter(function (){
                        return $(this).text().toLocaleLowerCase().indexOf(s) !== -1;
                    })
                    .addClass('found')
                    .siblings('.placeholder')
                    .each(function (){
                        open($(this));
                    });
                }
            },
            600);
        }).insertBefore($tree)
          .addClass('filterKeyword')
          .before('<label>' + filter_label + ' </label>');
        // placeholders
        $tree
            .addClass('collapsedtree')
            .find('li')
            .prepend('<span class="placeholder"></span>');

        //collapsing engine
        $tree
            .find('ul')
            .hide()
            .siblings('.placeholder')
            .addClass('handler')
            .click(function (){
                var $this = jQuery(this);
                if($this.is('.opened')){
                    close($this, 'fast');
                }
                else{
                    open($this, 'fast');
                }
                return false;
            });

    });

};


