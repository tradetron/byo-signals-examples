# Excel and Google Sheets

Use the sheet Signal Bridge makes for you: Done → **Excel** → Download Excel sheet. One row per symbol, a Quantity
cell, and coloured Buy / Exit buy / Sell / Exit sell buttons. Change the quantity, click a button: your browser opens
and shows `Ok`. It works in Excel on Windows and Mac and in Google Sheets, and it has **no macros**: each button is a
`HYPERLINK` to a signal link (see [`../links/`](../links/)).

The sheet carries your key inside every button. **Never share the file**, never put it in a shared drive or a
repository. If it has been shared, rotate the key (My Strategies → API button → unlink, link again) and download a
fresh sheet; the old one stops working.

There is no sheet in this repository on purpose: a sheet without your key does nothing, and a sheet with a key must
not be public.
