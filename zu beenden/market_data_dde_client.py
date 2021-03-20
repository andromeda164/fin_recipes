import win32ui
import dde

server = dde.CreateServer()
server.Create("IT2")

conversation = dde.CreateConversation(server)

conversation.ConnectTo("IT", "Price")
print conversation.Exec("OESX\X83500.00.EU,Last")
conversation.Exec("DoSomethingElse")

conversation.ConnectTo("RunAny", "ComputeStringLength")
s = 'abcdefghi'
sl = conversation.Request(s)
print 'length of "%s" is %s'%(s,sl)

