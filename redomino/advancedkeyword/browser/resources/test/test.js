$(document).ready(function (){
    $('.tree').keywordtree('.select');
    $('.tree').collapsedtree();
    function reset(){
        $('.tree :checked').removeAttr('checked');
    };
    module("Test keywordtree");
    test('checking A.A.B', function (){
        reset();
        $('#A-A-B').attr('checked','checked').click().attr('checked','checked');
        var values = $('.select').val();
        notEqual($.inArray('A', values), -1, 'select: A checked');
        notEqual($.inArray('A.A', values), -1, 'select: A.A checked');
        notEqual($.inArray('A.A.B', values), -1, 'select: A.A.B checked');
        equal($.inArray('A.B', values), -1, 'select: A.B not checked');
        equal($.inArray('B', values), -1, 'select: B not checked');
        equal($.inArray('B.A', values), -1, 'select: B.A not checked');
        equal($.inArray('A.A.A', values), -1, 'select: A.A.A not checked');

        ok($('.tree #A:checked').length === 1, 'checkboxes: #A checked');
        ok($('.tree #A-A:checked').length === 1, 'checkboxes: #A-A checked');
        ok($('.tree #A-A-B:checked').length === 1, 'checkboxes: #A-A-B checked');
        ok($('.tree #A-A-A:checked').length === 0, 'checkboxes: #A-A-A unchecked');
        ok($('.tree #A-B:checked').length === 0, 'checkboxes: #A-B unchecked');
    });

    test('checking B', function (){
        reset();
        $('#B').attr('checked','checked').click().attr('checked','checked');
        var values = $('.select').val();
        equal($.inArray('A', values), -1, 'select: A not checked');
        equal($.inArray('A.A', values), -1, 'select: A.A not checked');
        equal($.inArray('A.A.B', values), -1, 'select: A.A.B not checked');
        equal($.inArray('A.B', values), -1, 'select: A.B not checked');
        notEqual($.inArray('B', values), -1, 'select: B checked');
        equal($.inArray('B.A', values), -1, 'select: B.A not checked');
        equal($.inArray('A.A.A', values), -1, 'select: A.A.A not checked');

        ok($('.tree #A:checked').length === 0, 'checkboxes: #A unchecked');
        ok($('.tree #A-A:checked').length === 0, 'checkboxes: #A-A unchecked');
        ok($('.tree #A-A-B:checked').length === 0, 'checkboxes: #A-A-B unchecked');
        ok($('.tree #A-A-A:checked').length === 0, 'checkboxes: #A-A-A unchecked');
        ok($('.tree #A-B:checked').length === 0, 'checkboxes: #A-B unchecked');
        ok($('.tree #B:checked').length !== 0, 'checkboxes: #B checked');
    });

    test('checking A.A', function (){
        reset();
        $('#A-A').attr('checked','checked').click().attr('checked','checked');
        var values = $('.select').val();
        notEqual($.inArray('A', values), -1, 'select: A checked');
        notEqual($.inArray('A.A', values), -1, 'select: A.A checked');
        equal($.inArray('A.A.B', values), -1, 'select: A.A.B  not checked');
        equal($.inArray('A.B', values), -1, 'select: A.B not checked');
        equal($.inArray('B', values), -1, 'select: B not checked');
        equal($.inArray('B.A', values), -1, 'select: B.A not checked');
        equal($.inArray('A.A.A', values), -1, 'select: A.A.A not checked');

        ok($('.tree #A:checked').length !== 0, 'checkboxes: #A checked');
        ok($('.tree #A-A:checked').length !== 0, 'checkboxes: #A-A checked');
        ok($('.tree #A-A-B:checked').length === 0, 'checkboxes: #A-A-B unchecked');
        ok($('.tree #A-A-A:checked').length === 0, 'checkboxes: #A-A-A unchecked');
        ok($('.tree #A-B:checked').length === 0, 'checkboxes: #A-B unchecked');
        ok($('.tree #B:checked').length === 0, 'checkboxes: #B not checked');
    });

    test('checking A.A.B, unchecking A', function (){
        reset();
        $('#A-A-B').attr('checked','checked').click().attr('checked','checked');
        $('#A').removeAttr('checked').click().removeAttr('checked');
        var values = $('.select').val() || [];
        equal($.inArray('A', values), -1, 'select: A not checked');
        equal($.inArray('A.A', values), -1, 'select: A.A not checked');
        equal($.inArray('A.A.B', values), -1, 'select: A.A.B not checked');
        equal($.inArray('A.B', values), -1, 'select: A.B not checked');
        equal($.inArray('B', values), -1, 'select: B not checked');
        equal($.inArray('B.A', values), -1, 'select: B.A not checked');
        equal($.inArray('A.A.A', values), -1, 'select: A.A.A not checked');

        ok($('.tree #A:checked').length === 0, 'checkboxes: #A not checked');
        ok($('.tree #A-A:checked').length === 0, 'checkboxes: #A-A not checked');
        ok($('.tree #A-A-B:checked').length === 0, 'checkboxes: #A-A-B not checked');
        ok($('.tree #A-A-A:checked').length === 0, 'checkboxes: #A-A-A not checked');
        ok($('.tree #A-B:checked').length === 0, 'checkboxes: #A-B not checked');
    });


    test('checking A.A.B, unchecking A.A', function (){
        reset();
        $('#A-A-B').attr('checked','checked').click().attr('checked','checked');
        $('#A-A').removeAttr('checked').click().removeAttr('checked');
        var values = $('.select').val();
        notEqual($.inArray('A', values), -1, 'select: A checked');
        equal($.inArray('A.A', values), -1, 'select: A.A not checked');
        equal($.inArray('A.A.B', values), -1, 'select: A.A.B not checked');
        equal($.inArray('A.B', values), -1, 'select: A.B not checked');
        equal($.inArray('B', values), -1, 'select: B not checked');
        equal($.inArray('B.A', values), -1, 'select: B.A not checked');
        equal($.inArray('A.A.A', values), -1, 'select: A.A.A not checked');

        ok($('.tree #A:checked').length === 1, 'checkboxes: #A checked');
        ok($('.tree #A-A:checked').length === 0, 'checkboxes: #A-A not checked');
        ok($('.tree #A-A-B:checked').length === 0, 'checkboxes: #A-A-B not checked');
        ok($('.tree #A-A-A:checked').length === 0, 'checkboxes: #A-A-A not checked');
        ok($('.tree #A-B:checked').length === 0, 'checkboxes: #A-B not checked');
    });

    test('checking A.A.B, unchecking A.A.B', function (){
        reset();
        $('#A-A-B').attr('checked','checked').click().attr('checked','checked');
        $('#A-A-B').removeAttr('checked').click().removeAttr('checked');
        var values = $('.select').val();
        notEqual($.inArray('A', values), -1, 'select: A checked');
        notEqual($.inArray('A.A', values), -1, 'select: A.A checked');
        equal($.inArray('A.A.B', values), -1, 'select: A.A.B not checked');
        equal($.inArray('A.B', values), -1, 'select: A.B not checked');
        equal($.inArray('B', values), -1, 'select: B not checked');
        equal($.inArray('B.A', values), -1, 'select: B.A not checked');
        equal($.inArray('A.A.A', values), -1, 'select: A.A.A not checked');

        ok($('.tree #A:checked').length === 1, 'checkboxes: #A checked');
        ok($('.tree #A-A:checked').length === 1, 'checkboxes: #A-A checked');
        ok($('.tree #A-A-B:checked').length === 0, 'checkboxes: #A-A-B not checked');
        ok($('.tree #A-A-A:checked').length === 0, 'checkboxes: #A-A-A not checked');
        ok($('.tree #A-B:checked').length === 0, 'checkboxes: #A-B not checked');
    });
    test('checking A, checking A.A.B', function (){
        reset();
        $('#A').attr('checked','checked').click().attr('checked','checked');
        $('#A-A-B').attr('checked','checked').click().attr('checked','checked');
        var values = $('.select').val();
        notEqual($.inArray('A', values), -1, 'select: A checked');
        notEqual($.inArray('A.A', values), -1, 'select: A.A checked');
        notEqual($.inArray('A.A.B', values), -1, 'select: A.A.B checked');
        equal($.inArray('A.B', values), -1, 'select: A.B not checked');
        equal($.inArray('B', values), -1, 'select: B not checked');
        equal($.inArray('B.A', values), -1, 'select: B.A not checked');
        equal($.inArray('A.A.A', values), -1, 'select: A.A.A not checked');

        ok($('.tree #A:checked').length === 1, 'checkboxes: #A checked');
        ok($('.tree #A-A:checked').length === 1, 'checkboxes: #A-A checked');
        ok($('.tree #A-A-B:checked').length === 1, 'checkboxes: #A-A-B checked');
        ok($('.tree #A-A-A:checked').length === 0, 'checkboxes: #A-A-A unchecked');
        ok($('.tree #A-B:checked').length === 0, 'checkboxes: #A-B unchecked');
    });
    module("Test collapsedtree");
    asyncTest('test filter', function (){
        $('.filterKeyword').val('b').keyup();
        setTimeout(function (){
            $('.tree label').each(function (){
                var $this = $(this);
                if ($this.is('.found')){
                    ok($this.text() === 'B', 'B found');
                    //check the display
                    $this.parents('ul').each(function (){
                        ok($(this).is(':visible'),'node is visible');
                    });
                }
                else {
                    ok($this.text() === 'A', 'A not found');
                }
            });


            start();
        },700);

    });
    asyncTest('test filter (empty)', function (){
        $('.filterKeyword').val('').keyup();
        setTimeout(function (){
            ok($('.tree label.found').length === 0, 'not found');
            ok($('.tree ul:visible').length === 0, 'not found');

            start();
        },700);

    });
    asyncTest('test click', function (){
        var $placeholder = $('.tree .placeholder.handler').first();
        ok(! $placeholder.is('.opened'), 'is closed');
        ok(! $placeholder.siblings('ul').is(':visible'), 'is hidden');
        $('.filterKeyword').val('').keyup();
        setTimeout(function (){
            $placeholder.click();
            ok($placeholder.is('.opened'), 'is opened');
            ok($placeholder.siblings('ul').is(':visible'), 'is visible');

            start();
        },700);

    });

});
