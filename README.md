# NexTrace

**NexTrace** is a Python-based phone number intelligence tool designed for learning about OSINT, phone number metadata, and privacy-aware analysis.

The project currently provides a terminal interface with colored output, phone number validation, messaging links, and JSON report exports.

> **Status:** Early development — features and documentation may change.

## Features

- Phone number parsing and formatting
- Country and calling code detection
- Number type and validity checks
- Available carrier and time zone metadata
- WhatsApp direct-link generation
- Telegram link generation
- JSON report export
- Colored command-line interface
- No paid API key required

## Requirements

- Python 3.10 or newer
- `phonenumbers`
- `colorama`

## Installation

Clone the repository:

```bash
git clone https://github.com/Nexform-star/NexTrace.git
cd NexTrace
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Run NexTrace:

```bash
python nextrace.py
```

Enter a phone number in international format when prompted, for example:

```text
+33XXXXXXXXX
```

Replace the example with a number you are authorized to analyze.

## Project Structure

```text
NexTrace/
├── nextrace.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Limitations

NexTrace uses locally available numbering metadata provided by the `phonenumbers` library.

- A valid number format does not prove that a number is active or assigned.
- Carrier information may be missing, outdated, or affected by number portability.
- Geographic descriptions are not precise GPS locations.
- A WhatsApp link does not confirm that a number has a WhatsApp account.
- A Telegram link does not guarantee that a profile can be found.
- NexTrace does not verify a subscriber's identity or bypass platform privacy settings.

## Privacy and Responsible Use

Use NexTrace only for lawful and legitimate purposes.

- Analyze numbers you own or are authorized to check.
- Do not use the tool to harass, stalk, or identify private individuals without authorization.
- Do not publish personal phone numbers or reports containing private information.
- Respect applicable laws, platform terms, and privacy settings.

## Roadmap

- [x] Initial phone number analysis
- [x] Colored command-line interface
- [x] WhatsApp link generation
- [x] Telegram link generation
- [x] JSON report export
- [ ] Improve error handling and validation
- [ ] Add privacy-aware public spam reputation sources
- [ ] Improve report formatting

## Contributing

Suggestions, bug reports, and contributions are welcome. Please ensure that proposed features respect privacy and platform rules.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for details, if included.
