    //////////////////// Custom JS ////////////////////////// 
    // If user field in not empty then action will works
    function validateForm() {
        var x1 = document.forms["myForm"]["name"].value;
        var x2 = document.forms["myForm"]["userid"].value;
        var x3 = document.forms["myForm"]["emailAdress"].value;
        var x4 = document.forms["myForm"]["password"].value;
        var x5 = document.forms["myForm"]["passwordCon"].value;
        if (x1 == "" || x1 == null) {
            // alert("Name must be filled out");
        } else if (x2 == "" || x2 == null) {
            // alert("User id must be filled out");
        } else if (x3 == "" || x3 == null) {
            // alert("Email Adress must be filled out");
        } else if (x4 == "" || x4 == null) {
            // alert("Password must be filled out");
        } else if (x5 == "" || x5 == null) {
            // alert("Password must be filled out");
        } else {
            document.getElementById("myForm").submit();
            // event.preventDefault();
        }
    }

    // Switch to Log-in Page 
    function switchMe() {
        document.getElementById("haveAccount").click();
    }

    //////////////////// Custom JS ////////////////////////// 

// .................Toggle Button..................... 
const toggleButton = document.getElementsByClassName('toggle-button')[0]
const navbarLinks = document.getElementsByClassName('navbar-links')[0]

toggleButton.addEventListener('click', () => {
  navbarLinks.classList.toggle('active')
})
// ..................Toggle Button.................... 

/*global $, document, window, setTimeout, navigator, console, location*/
$(document).ready(function () {

    'use strict';

    var usernameError = true,
        useridError    = true,
        emailError    = true,
        passwordError = true,
        passConfirm   = true;

    // Detect browser for css purpose
    if (navigator.userAgent.toLowerCase().indexOf('firefox') > -1) {
        $('.form form label').addClass('fontSwitch');
    }

    // Label effect
    $('input').focus(function () {

        $(this).siblings('label').addClass('active');
    });

    // Form validation
    $('input').blur(function () {
        // ........................................ 
        // User Id 
        if ($(this).hasClass('userid')) {
            if ($(this).val().length === 0) {
                $(this).siblings('span.error').text('Please type your username').fadeIn().parent('.form-group').addClass('hasError');
                useridError = true;
            } else if ($(this).val().length > 1 && $(this).val().length <= 6) {
                $(this).siblings('span.error').text('Please type at least 6 characters').fadeIn().parent('.form-group').addClass('hasError');
                useridError = true;
            } else {
                $(this).siblings('.error').text('').fadeOut().parent('.form-group').removeClass('hasError');
                useridError = false;
            }
        }
        // ........................................ 
        // User Name
        if ($(this).hasClass('name')) {
            if ($(this).val().length === 0) {
                $(this).siblings('span.error').text('Please type your full name').fadeIn().parent('.form-group').addClass('hasError');
                usernameError = true;
            } else if ($(this).val().length > 1 && $(this).val().length <= 6) {
                $(this).siblings('span.error').text('Please type at least 6 characters').fadeIn().parent('.form-group').addClass('hasError');
                usernameError = true;
            } else {
                $(this).siblings('.error').text('').fadeOut().parent('.form-group').removeClass('hasError');
                usernameError = false;
            }
        }
        // Email
        if ($(this).hasClass('email')) {
            if ($(this).val().length == '') {
                $(this).siblings('span.error').text('Please type your email address').fadeIn().parent('.form-group').addClass('hasError');
                emailError = true;
            } else {
                $(this).siblings('.error').text('').fadeOut().parent('.form-group').removeClass('hasError');
                emailError = false;
            }
        }

        // PassWord
        if ($(this).hasClass('pass')) {
            if ($(this).val().length < 8) {
                $(this).siblings('span.error').text('Please type at least 8 charcters').fadeIn().parent('.form-group').addClass('hasError');
                passwordError = true;
            } else {
                $(this).siblings('.error').text('').fadeOut().parent('.form-group').removeClass('hasError');
                passwordError = false;
            }
        }

        // PassWord confirmation
        if ($('.pass').val() !== $('.passConfirm').val()) {
            $('.passConfirm').siblings('.error').text('Passwords don\'t match').fadeIn().parent('.form-group').addClass('hasError');
            passConfirm = false;
        } else {
            $('.passConfirm').siblings('.error').text('').fadeOut().parent('.form-group').removeClass('hasError');
            passConfirm = false;
        }

        // label effect
        if ($(this).val().length > 0) {
            $(this).siblings('label').addClass('active');
        } else {
            $(this).siblings('label').removeClass('active');
        }
    });


    // form switch
    $('a.switch').click(function (e) {
        $(this).toggleClass('active');
        e.preventDefault();

        if ($('a.switch').hasClass('active')) {
            $(this).parents('.form-peice').addClass('switched').siblings('.form-peice').removeClass('switched');
        } else {
            $(this).parents('.form-peice').removeClass('switched').siblings('.form-peice').addClass('switched');
        }
    });


    // Form submit
    // $('form.signup-form').submit(function (event) {
    //     event.preventDefault();

    //     if (usernameError == true || useridError == true || emailError == true || passwordError == true || passConfirm == true) {
    //         $('.name, .userid, .email, .pass, .passConfirm').blur();
    //     } else {
    //         $('.signup, .login').addClass('switched');

    //         setTimeout(function () { $('.signup, .login').hide(); }, 700);
    //         setTimeout(function () { $('.brand').addClass('active'); }, 300);
    //         setTimeout(function () { $('.heading').addClass('active'); }, 600);
    //         setTimeout(function () { $('.success-msg p').addClass('active'); }, 900);
    //         setTimeout(function () { $('.success-msg a').addClass('active'); }, 1050);
    //         setTimeout(function () { $('.form').hide(); }, 700);
    //     }
    // });

    // Reload page
    $('a.profile').on('click', function () {
        location.reload(false);
    });


});