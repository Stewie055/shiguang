from utils import clean_html

str = '''<b>redy</b>
        <img src="data:image/jpeg;base64,">
        <<script></script>script> alert("Haha, I hacked your page."); <<script></script>script>
        '''
html = '''
        both <em id="foo" style="color: black">can</em> have
                     <img id="bar" src="foo"/>
   <script type="text/javascript" src="evil-site"></script>
   <link rel="alternate" type="text/rss" src="evil-rss">
   <style>
     body {background-image: url(javascript:do_evil)};
     div {color: expression(evil)};
   </style>
 < onload="evil_function()">
    <!-- I am interpreted for EVIL! -->
   <img src="">
   <a href="javascript:evil_function()">a link</a>
   <a href="#" onclick="evil_function()">another link</a>
   <p onclick="evil_function()">a paragraph</p>
   <div style="display: none">secret EVIL!</div>
   <object> of EVIL! </object>
   <iframe src="evil-site"></iframe>
   <form action="evil-site">
     Password: <input type="password" name="password">
   </form>
   <blink>annoying EVIL!</blink>
   <a href="evil-site">spam spam SPAM!</a>
   <image src="evil!">
</html>''' + str
print(clean_html(html))
