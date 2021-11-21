# Plan json

Frontend to backend request example request.

```json
{
  "degree_details": {
	"degree_code": 1234,
	"selected_courses": [
	  "COMP1511",
	  "COMP1521",
	  "COMP1531",
	  "COMP2521",
	  "MATH1081",
	  "MATH1141"
	]
  },
  "plan_details": {
	"starting_term": 1,
	"swap_limit": 3,
	"optimal_parameters": [
	  "difficulty",
	  "term_balance"
	]
  },
  "plan": [
	{
	  "max_uoc": 20,
	  "courses": [
		"COMP1511",
		"MATH1081",
		"MATH1141"
	  ]
	},
	{
	  "max_uoc": 12,
	  "courses": [
		"COMP2521"
	  ]
	},
	{
	  "max_uoc": 20,
	  "courses": [
		"COMP1521",
		"COMP1531"
	  ]
	},
	{
	  "max_uoc": 0,
	  "courses": [
	  ]
	}
  ]
}
```


