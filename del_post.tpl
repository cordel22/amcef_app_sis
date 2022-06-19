%#template for editing a task
%#the template expects to receive a value for "no" as well a "old", the text of the selected ToDo item
<p>You are about todelete post with ID = {{no}}</p>
<table border="1">
  <tr>
      <th>user_id</th>
      <th>id</th>
      <th>title</th>
      <th>body</th>
      <th>date</th>
  </tr>

  <tr>
    <td>{{old["user_id"]}}</td>
    <td>{{old["id"]}}</td>
    <td>{{old["title"]}}</td>
  
    <td>{{old["body"]}}</td>
    <td>{{old["date"]}}</td>
  
</tr>

</table>
<form action="/del_post/{{no}}" method="get">
  <!--
  <input type="text" name="title" value="{{old["title"]}}" size="100" maxlength="100">
  <select name="status">
    <option>open</option>
    <option>closed</option>
  <input type="text" name="body" value="{{old["body"]}}" size="100" maxlength="100">
  <select name="status">
    <option>open</option>
    <option>closed</option>
  </select>-->
  <br>
  
  <!--  <input type="hidden" name="id" value="{{no}}">
  <input type="hidden" name="id" value="{{no}}">-->
  Confirm the ID you want to get rid off:
  <input type="text" name="id" value="{{no}}">
  <input type="submit" value="delete">
</form>