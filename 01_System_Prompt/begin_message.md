# Begin Message (Retell "Welcome Message" / "AI speaks first")

Set the agent to **speak first** and paste the line for the language under test. Retell substitutes `{{variables}}` in the begin message the same way as in the prompt.

## English (language_to_speak = English)
```
Hello, good {{time_of_day}}! Am I speaking with {{customer_name}}?
```
`time_of_day` is an optional helper variable (morning / afternoon / evening). If you don't want an extra variable, use:
```
Hello! Am I speaking with {{customer_name}}?
```

## Hindi (language_to_speak = Hindi)
```
नमस्ते! क्या मेरी बात {{customer_name}} जी से हो रही है?
```

Notes
- The begin message only asks for identity. The agent introduces itself and the offer **after** the customer confirms, so nothing is disclosed to a wrong person.
- Keep the begin message identical across all recorded calls of the same language.
