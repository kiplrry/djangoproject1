/// <reference path="./jquery.js" />
/// <reference path="./bootstrap.bundle.js" />
$(function(){
    function getTodos(){
        let url = '/todos/all'
        let data = ''
        $.get(url, function(da){
            data = da;
            $('#all-todos').html(da)
            console.log('refresh')
        });
    }
    getTodos()

    $('#all-todos').on('submit', '.modal-edit',function(e){
        let todoModal = new bootstrap.Modal('#todoModal')
        e.preventDefault()
        var formData = $(this).serialize();
        console.log(formData)
        $.post($(this).attr('action'), formData, function(r){
            $('#todoModal').html(r)
            console.log(todoModal)
            todoModal.show()
        })
    })
    $('#all-todos').on('submit', '.editing',  function(e){
        e.preventDefault()
        var formData = $(this).serialize();
        console.log(formData)
        $.post($(this).attr('action'), formData, function(r){
            getTodos()
        })
    })
    $('#add-task').on('submit', function(e){
        e.preventDefault()
        var formData = $(this).serialize();
        console.log(formData)
        $.post($(this).attr('action'), formData, function(r){
            getTodos()
        })
        $('#task-input').val('')
    })
    $('body').on('submit', '#todo-form',function(e){
        e.preventDefault()
        var formData = $(this).serialize();
        console.log($(this).attr('action'))
        $.post($(this).attr('action'), formData, function(r){
            getTodos()
            console.log(formData)
        })
    })
    function getFiltered(e){
        e.preventDefault()
        console.log(this)
        var formData = $(this).serialize();
        $.get($(this).attr('action'), formData, function(da){
            $('#all-todos').html(da)
            // console.log(da)
        });
    }
    $('body').on('submit', '#search-todos',function(e){
        getFiltered.bind(this)(e)
    })
    $("#search").on('input', function(e){
        // if($(this).val().trimStart()){
        //     getFiltered.bind(this)(e)
        // } else{
        //     getTodos()
        // }
        var value = $(this).val().toLowerCase();

        $("#list-group .todo-text").filter(function() {
            // $(this).parent().toggle(true)
            $(this).parent().toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    })
});
