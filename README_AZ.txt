MY CYBER LAB — təhlükəsiz təlim nümunəsi

Bu tətbiq yalnız ləqəb və təlim kodu saxlayır. Real şifrə, təsdiq kodu və ya hesab məlumatı istəmir.

Termux-da:
1) pkg update
2) pkg install python
3) pip install flask
4) Layihə qovluğuna keç.
5) Təkcə öz cihazında sınaq üçün:
   export ADMIN_PASSWORD='ozun-secdiyin-guclu-admin-parolu'
   export FLASK_SECRET_KEY='uzun-tesadufi-məxfi-açar'
   python app.py
6) Brauzerdə http://127.0.0.1:8081 aç.
7) İdarəçi paneli: http://127.0.0.1:8081/admin/login

Vacib:
- Flask development server-i internetə açma.
- İctimai yayımlamaq üçün təhlükəsiz hosting, HTTPS, güclü gizli açarlar,
  giriş məhdudiyyəti və iştirakçıların məlumatlandırılması lazımdır.
- Bu nümunəni real hesab giriş səhifəsi kimi təqdim etmə.
