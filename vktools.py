import vk
from functools import reduce


class vktools(object):
    def __init__(self, token, version='5.102', lang='ru'):
        self.session = vk.Session(access_token=token)
        self.api = vk.API(self.session)
        self.version = version
        self.lang = lang

    def Friends(self, ids, print=True):
        try:
            friends = [set(self.api.friends.get(user_id=userid, v=self.version)['items']) for userid in ids]
            friends = list(reduce(lambda x, y: x | y, friends))
            if print:
                self.Print(friends, line='Friends of ' + self.GetNameLine(ids) + ':')
            return friends
        except vk.exceptions.VkAPIError:
            if print:
                self.Print([], line='Error in Friends func(VkAPIError)')
            return []

    def AllFriends(self, target, ids=[], print=True):
        friends = set(self.Friends(target, print=False))
        queue = list(friends) + ids
        while queue:
            last = queue.pop()
            if last not in friends and target[0] in self.Friends([last], print=False):
                friends.add(last)
            for userid in self.MutualFriends([target[0], last], print=False):
                if userid not in friends:
                    friends.add(userid)
                    queue.append(userid)
        friends = list(friends)
        if print:
            self.Print(friends, line='AllFriends of ' + self.GetName(target)[0] + ':')
        return friends

    def HiddenFriends(self, target, ids=[], print=True):
        friends = list(set(self.AllFriends(target, ids=ids, print=False)) - set(self.Friends([target], print=False)))
        if print:
            self.Print(friends, line='HiddenFriends of ' + self.GetName(target)[0] + ':')
        return friends

    def LimitedMutualFriends(self, ids, print=True):
        friends = list(reduce(lambda x, y: x & y, [set(self.Friends([userid], print=False)) for userid in ids]))
        if print:
            self.Print(friends, line='LimitedMutualFriends of ' + self.GetNameLine(ids) + ':')
        return friends

    def UnlimitedMutualFriends(self, ids, print=True):
        friends = {userid: self.Friends([userid], print=False) for userid in ids}
        result = set()
        for key, value in friends.items():
            for friend in value:
                newfriends = set(self.Friends([friend], print=False))
                newfriends.add(key)
                if set(ids).issubset(newfriends):
                    result.add(friend)
        friends = list(result)
        if print:
            self.Print(friends, line='UnlimitedMutualFriends of ' + self.GetNameLine(ids) + ':')
        return friends

    def MutualFriends(self, ids, print=True):
        friends = list(set(self.LimitedMutualFriends(ids, print=False)) | set(self.UnlimitedMutualFriends(ids, print=False)))
        if print:
            self.Print(friends, line='MutualFriends of ' + self.GetNameLine(ids) + ':')
        return friends

    def GroupFriends(self, ids, groups, print=True):
        friends = self.Friends(ids, print=False)
        groups = self.GetGroupId(groups)
        result = set()
        for groupid in groups:
            try:
                res = [ans['member'] for ans in self.api.groups.isMember(user_ids=friends, group_id=groupid, v=self.version)]
                result |= set(i[0] for i in zip(friends, res) if i[1])
            except vk.exceptions.VkAPIError:
                continue
        self.Print(list(result), 'GroupFriends of ' + self.GetNameLine(ids) + ':')
        return list(result)

    def GetInfo(self, ids):
        try:
            return [self.api.users.get(user_ids=userid, v=self.version, lang=self.lang) for userid in ids]
        except vk.exceptions.VkException:
            return []

    def GetName(self, ids):
        return [userinfo[0]['first_name'] + ' ' + userinfo[0]['last_name'] for userinfo in self.GetInfo(ids)]

    def GetLink(self, ids):
        return ['https://vk.com/id' + str(userid) for userid in self.GetUserId(ids)]

    def GetGroupId(self, groups):
        try:
            return [group['id'] for group in self.api.groups.getById(group_ids=groups, v=self.version)]
        except vk.exceptions.VkAPIError:
            return []

    def GetUserId(self, ids):
        return [userinfo[0]['id'] for userinfo in self.GetInfo(ids)]

    def GetNameLine(self, ids):
        line = ''
        for i in ids:
            line += self.GetName([i])[0] + ', '
        line = line[:-2]
        return line

    def Print(self, ids, line=''):
        if line:
            print(line)
        names = self.GetName(ids)
        links = self.GetLink(ids)
        for name, link in zip(names, links):
            print(f'{name:<40} : {link}')
