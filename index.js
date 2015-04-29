var request = require('request-promise');
var sendgrid  = require('sendgrid')(process.env.SendGridTechatNYUUser, process.env.SendGridTechatNYUKey);

var attendeeById = {};

var sendEmail = function(singleAttendee){
  var email = new sendgrid.Email();

  // The previous randomSelect makes sure this exists
  email.addTo(singleAttendee.contact.email);
  email.from = 'feedback@techatnyu.org';
  
  // These are what the template replaces.
  email.subject = 'Tech@NYU - Hello!';
  email.text = ':)'

  // Attach template to the event
  email.addFilter('templates', 'enable', 1);
  email.addFilter('templates', 'template_id', '16437110-b76a-4269-a660-ac03d6fbefb6');

  sendgrid.send(email, function(err, json){
    if(err) return console.error(err);
    console.log(json);
  });
};

var randomSelect = function(allAttendees){
  var filterSet = [];
  allAttendees.forEach(function(singleAttendee){
    if(attendeeById[singleAttendee.id] && attendeeById[singleAttendee.id].contact && attendeeById[singleAttendee.id].contact.email){
      filterSet.push(attendeeById[singleAttendee.id]);
    }
  });
  return filterSet;
};

request({
  rejectUnauthorized: false,
  url: 'https://api.tnyu.org/v2/events?sort=-startDateTime&include=attendees', 
  headers: {
    'x-api-key': process.env.ApiKey,
    'accept': 'application/vnd.api+json'
  },
  timeout: 100000
}).then(function(body){
  var apiJSON = JSON.parse(body);
  var events = apiJSON.data;
  var attendees = apiJSON.included;

  attendees.forEach(function(singleAttendee){
    attendeeById[singleAttendee.id] = singleAttendee;
  });

  events.forEach(function(singleEvent){
    if(singleEvent.id == "554118960225415a1b9b8a75"){
      var subsetAttendees = randomSelect(singleEvent.links && singleEvent.links.attendees && singleEvent.links.attendees.linkage)
      subsetAttendees.forEach(function(singleAttendee){
        sendEmail(singleAttendee);
      });
    }
  });
})