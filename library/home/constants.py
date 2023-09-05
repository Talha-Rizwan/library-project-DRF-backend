'''Constants used in the home application.'''
PENDING_STATUS = 'P'
APPROVED_STATUS = 'A'
REJECTED_STATUS = 'R'
RETURN_BACK_STATUS = 'B'
CLOSED_STATUS = 'C'

STATUS_CHOICES = (
    (PENDING_STATUS, 'Pending'),
    (APPROVED_STATUS, 'Approved'),
    (REJECTED_STATUS, 'Rejected'),
    (RETURN_BACK_STATUS, 'Back Return'),
    (CLOSED_STATUS, 'Closed')
)

TICKET_STATUS_CHOICES = (
        (PENDING_STATUS, 'Pending'),
        (APPROVED_STATUS, 'Approved'),
        (REJECTED_STATUS, 'Rejected')
    )

ADMIN_EMAIL = 'admin@gmail.com'

LIBRARIAN_EMAIL = 'librarian@gmail.com'

DELAYED_REQUEST_DAYS = 1
