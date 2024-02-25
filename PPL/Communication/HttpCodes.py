# -*- coding: utf-8 -*-
#  Copyleft  2021-2024 Mattijs Snepvangers.
#  This file is part of Pegasus-ICT Python Library, hereafter named PPL.
#
#  PPL is free software: you can redistribute it and/or modify  it under the terms of the
#   GNU General Public License as published by  the Free Software Foundation, either version 3
#   of the License or any later version.
#
#  PPL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#   without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE.  See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#   along with PPL.  If not, see <https://www.gnu.org/licenses/>.
class HTTPCodes:
    CODES = {
        100: "Continue",
        101: "Switching Protocols",
        102: "DEPRECATED: WEBDAV Processing",
        103: "Early hints",

        200: "OK",
        201: "Created",
        202: "Accepted",
        203: "Non-Authoritative Information",
        204: "No Content",
        205: "Reset Content",
        206: "Partial Content",
        207: "WEBDAV: Multi-Status",
        208: "WEBDAV: Already Reported",
        218: "Apache: This Is Fine",
        # RFC 3229
        226: "InstanceManipulation Used",

        300: "Multiple Choices",
        301: "Moved Permanently",
        302: "Found",
        303: "See Other",
        304: "Not Modified",
        305: "Use Proxy",
        306: "Switch Proxy",
        307: "Temporary Redirect",
        308: "Permanent Redirect",

        400: "Bad Request",
        401: "Unauthorized",
        402: "Payment Required",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        406: "Not Acceptable",
        407: "Proxy Authentication Required",
        408: "Request Timeout",
        409: "Conflict",
        410: "Gone",
        411: "Length Required",
        412: "Precondition Failed",
        413: "Payload Too Large",
        414: "URI Too Long",
        415: "Unsupported Media Type",
        416: "Range Not Satisfiable",
        417: "Expectation Failed",
        418: "I'm A Teapot",
        419: "Laravel: Page Expired",
        420: "Twitter: Enhance Your Calm",
        421: "Misdirected Request",
        422: "Unprocessable Content",
        423: "WEBDAV: Locked",
        424: "WEBDAV: Failed Dependency",
        425: "Too Early",
        426: "Upgrade Required",
        428: "Precondition Required",
        429: "Too Many Requests",
        430: "Shopify Security Rejection",
        431: "Request Header Fields Too Large",
        450: "Blocked By Windows Parental Controls",
        451: "Unavailable For Legal Reasons",
        498: "ESRI: Invalid Token",
        499: "ESRI: Token Required",

        500: "Internal Server Error",
        501: "Not Implemented",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
        505: "HTTP Version Not Supported",
        506: "Variant Also Negotiates",
        507: "WEBDAV Insufficient Storage",
        508: "WEBDAV Loop Detected",
        509: "Bandwidth Limit Exceeded",
        510: "Not Extended",
        511: "Network Authentication Required",
        529: "Site Is Overloaded",
        530: "Either Site Is Frozen Or Shopify Origin DNS Error",
        540: "Shopify Temporarily Disabled",
        598: "(Informal Convention) Network Read Timeout Error",
        599: "Network Connect Timeout Error",

        783: "Shopify Unexpected Token"
    }
