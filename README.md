<h1>Letschat</h1>
<p>Letschat is my professionnal programming project, it's a django messaging app. It has 4 main features, user management, a friend system, public and private chat rooms </p>
<p>To access the features a user need to be authenticated. </p>
<h2>Programming languages used</h2>
<p>Django, HTML, CSS, Javascript, Python, Bootstrap</p>
<h2>Important libraries</h2> 
<p><a href="https://channels.readthedocs.io/en/latest/installation.html">python -m pip install -U 'channels[daphne]'</a>; This installs Channels together with the Daphne ASGI application server, with this library we can create live chat applications. </p>
<p><a href="https://pypi.org/project/crispy-bootstrap4/">pip install crispy-bootstrap4</a>; Bootstrap4 template pack for django-crispy-forms.</p>
<p><a href="https://pypi.org/project/pillow/">pip install pillow</a>; Pillow is a library that adds image processing capabilities to Django. </p>
<h3>User management</h3>
<ul>
  <li>Registration</li>
  <li>Login</li>
  <li>Logout</li>
  <li>Registration</li>
  <li>User profile</li>
  <li>Update profile</li>
  <li>Search user</li>
</ul>
<h3>Friend system</h3>
<ul>
  <li>Send friend requests</li>
  <li>Accept friend requests</li>
  <li>Cancel friend requests</li>
  <li>Deny friend requests</li>
  <li>remove friend</li>
  <li>Search friend</li>
</ul>
<h3>Public chat room</h3>
<ul>
  <li>Create public chat room</li>
  <li>Search public chat room</li>
  <li>Can send text, images or both</li>
  <li>Any authenticated user can create a public chat room where anyone can chat (Django channels & Websockets)</li>
</ul>
<h3>Private chat room</h3>
<ul>
  <li>Create private group chats</li>
  <li>Can send text, images or both</li>
  <li>Any authenticated user can create a private group chat which can contain from 1 friend to every friends of their friend list (Django channels & Websockets)</li>
</ul>
</hr>
