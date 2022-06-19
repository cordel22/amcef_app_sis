%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
      <div>
        <a href="logout">Log Out!</a>
      </div>
            <div>
        <h3>
         Welcome {{user["name"]}}, your email is {{user["email"]}}
         </h3>
      <div>
      <div>
      <p>Press to Add Post 
        <button onclick="window.location.href='/new/{{user["id"]}}';">
          Add Post
        </button>
      <p>
      </div>
      
<p>The forum posts in our DB are as follows:</p>
<table border="1">
  <tr>
      <th>user_id</th>
      <th>id</th>
      <th>title</th>
      <th>body</th>
      <th>date</th>
      <th>misc</th>
  </tr>
% # print({{forum}})
    % for i in range(len(rows)):
    %   if rows[i]["user_id"] == user["id"]:
    <tr>
      <td>{{rows[i]["user_id"]}}</td>
      <td>{{rows[i]["id"]}}</td>
      <td>{{rows[i]["title"]}}</td>
    
      <td>{{rows[i]["body"]}}</td>
      <td>{{rows[i]["date"]}}</td>
      <td>
        <button onclick="window.location.href='/edit/{{rows[i]["id"]}}';">
          Edit
        </button>
        <button onclick="window.location.href='/del_post/{{rows[i]["id"]}}';">
          Delete
        </button>
      </td>

    %   else:
      <tr>
      <td>{{rows[i]["user_id"]}}</td>
      <td>{{rows[i]["id"]}}</td>
      <td>{{rows[i]["title"]}}</td>
    
      <td>{{rows[i]["body"]}}</td>
      <td>{{rows[i]["date"]}}</td>
    % end
  </tr>
%end
</table>