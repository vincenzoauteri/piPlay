/** @jsx React.DOM */
var HelloMessage = React.createClass({displayName: 'HelloMessage',
    render: function() {
          return React.DOM.div(null, "Hello ", this.props.name);
            }
});

React.renderComponent(HelloMessage( {name:"World"} ), document.getElementById("testDiv"));
