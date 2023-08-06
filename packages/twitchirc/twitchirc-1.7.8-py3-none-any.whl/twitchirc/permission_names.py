#  Library to make crating bots for Twitch chat easier.
#  Copyright (c) 2019 Maciej Marciniak
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Names for permissions.

:py:const:`LOCAL_BYPASS_PERMISSION_TEMPLATE` Template for local bypass permissions.

:py:const:`GLOBAL_BYPASS_PERMISSION` Permission for bypassing every other

:py:const:`PERMISSION_COMMAND_PERM` Permission for the stock !perm command.

:py:const:`PERMISSION_COMMAND_PERM_ADD` Permission for adding permissions using !perm -a.

:py:const:`PERMISSION_COMMAND_PERM_REMOVE` Permission for adding permissions using !perm -r.

:py:const:`PERMISSION_COMMAND_PERM_LIST` Permission for adding permissions using !perm -l.

:py:const:`PERMISSION_COMMAND_QUIT` Permission for the stock !quit command.

:py:const:`PERMISSION_COMMAND_PART` Permission for the stock !part command.

:py:const:`PERMISSION_COMMAND_PART_OTHER` Permission for parting other channels using the !part command.

:py:const:`PERMISSION_COMMAND_JOIN` Permission for the stock !join command.

:py:const:`GROUP_PARENT` Template for creating permissions for inheritance.
"""
LOCAL_BYPASS_PERMISSION_TEMPLATE = 'twitchirc.bypass.permission.local.{}'
GLOBAL_BYPASS_PERMISSION = 'twitchirc.bypass.permission'

PERMISSION_COMMAND_PERM = 'twitchirc.perm'
PERMISSION_COMMAND_PERM_ADD = 'twitchirc.perm.add'
PERMISSION_COMMAND_PERM_REMOVE = 'twitchirc.perm.remove'
PERMISSION_COMMAND_PERM_LIST = 'twitchirc.perm.list'

PERMISSION_COMMAND_QUIT = 'twitchirc.quit'
PERMISSION_COMMAND_PART = 'twitchirc.part'
PERMISSION_COMMAND_PART_OTHER = 'twitchirc.part.other'
PERMISSION_COMMAND_JOIN = 'twitchirc.join'

GROUP_PARENT = 'parent.{}'
